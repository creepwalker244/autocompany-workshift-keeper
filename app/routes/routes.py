from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.time_records import WorkShift, Break, DeliveryTrip
from app.models.schemas import WorkShiftSchema, BreakSchema, DeliveryTripSchema
from datetime import datetime
from app.models.users import Role, User
from app.services.time_service import TimeCalculator
from app.services.db_init import get_db
from app.services.security import get_current_active_user

        
router = APIRouter()

@router.post(
    "/work_shifts/",
    response_model=dict,
    tags=["Work Shifts"],
    summary="Создать запись о рабочей смене",
    description="Добавляет новую запись о рабочих часах сотрудника",
    responses={
        200: {"description": "Успешное создание записи"},
        400: {"description": "Некорректные данные"}
    }
)
async def create_work_shift(
    work_shift: WorkShiftSchema, 
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """ 
        создание записи о рабочих часах
    """
    if current_user.role not in [Role.ADMIN, Role.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    db_work_shift = await WorkShift.insert_work_shift(session, 
                                                    user_id=work_shift.user_id,
                                                    start_time=work_shift.start_time,
                                                    end_time=work_shift.end_time)
    
    # Проверка времени
    if work_shift.start_time >= work_shift.end_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )
    
    return {"message": "Work shift created successfully", "data": {"id": db_work_shift.id}}

@router.post("/abreaks/")
async def create_abreak(abreak: BreakSchema, session: AsyncSession = Depends(get_db)):
    """
    создание записи о перерыве
    """
    db_abreak = await abreak.insert_abreak(session,
                                     user_id=abreak.user_id,
                                     start_time=abreak.start_time,
                                     end_time=abreak.end_time)
    return {"message": "abreak created successfully", "data": {"id": db_abreak.id}}

@router.post("/delivery_trips/")
async def create_delivery_trip(delivery_trip: DeliveryTripSchema, session: AsyncSession = Depends(get_db)):
    """
    создание записи о доставке
    """
    db_trip = await DeliveryTrip.insert_delivery_trip(session,
                                                    driver_id=delivery_trip.driver_id,
                                                    start_time=delivery_trip.start_time,
                                                    end_time=delivery_trip.end_time)
    return {"message": "Delivery trip created successfully", "data": {"id": db_trip.id}}

@router.get("/total_worked_time/")
async def get_total_worked_time(user_id: int, start: datetime, end: datetime, session: AsyncSession = Depends(get_db)):
    """
    получение общего времени, которое работник отработал
    """
    calculator = TimeCalculator(session)
    result = await calculator.calculate_work_time(user_id, start, end)
    return result

@router.get("/work_shifts/")
async def get_all_work_shifts(session: AsyncSession = Depends(get_db)):
    """
    получение всех записей о рабочих часах
    """
    async with session as session:
        work_shifts = select(WorkShift)
        work_shifts = await session.execute(work_shifts)
        work_shifts = work_shifts.scalars().all()
        
        return work_shifts

@router.get("/abreaks/")
async def get_all_abreaks(session: AsyncSession = Depends(get_db)):
    """
    получение всех записей о перерывах
    """
    abreaks = await session.query(Break).all()
    return {"data": abreaks}

@router.get("/delivery_trips/")
async def get_all_delivery_trips(session: AsyncSession = Depends(get_db)):
    """
    получение всех записей о доставках
    """
    delivery_trips = await session.query(DeliveryTrip).all()
    return {"data": delivery_trips}