from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..models.time_records import WorkShift, abreak, DeliveryTrip
from ..models.schemas import WorkShiftSchema, abreakSchema, DeliveryTripSchema
from ..app import get_db
from ..services.time_service import TimeCalculator

router = APIRouter()

@router.post("/work_shifts/")
async def create_work_shift(work_shift: WorkShiftSchema, session: AsyncSession = Depends(get_db)):
    db_work_shift = await WorkShift.insert_work_shift(session, 
                                                    user_id=work_shift.user_id,
                                                    start_time=work_shift.start_time,
                                                    end_time=work_shift.end_time)
    return {"message": "Work shift created successfully", "data": {"id": db_work_shift.id}}

@router.post("/abreaks/")
async def create_abreak(abreak: abreakSchema, session: AsyncSession = Depends(get_db)):
    db_abreak = await abreak.insert_abreak(session,
                                     user_id=abreak.user_id,
                                     start_time=abreak.start_time,
                                     end_time=abreak.end_time)
    return {"message": "abreak created successfully", "data": {"id": db_abreak.id}}

@router.post("/delivery_trips/")
async def create_delivery_trip(delivery_trip: DeliveryTripSchema, session: AsyncSession = Depends(get_db)):
    db_trip = await DeliveryTrip.insert_delivery_trip(session,
                                                    driver_id=delivery_trip.driver_id,
                                                    start_time=delivery_trip.start_time,
                                                    end_time=delivery_trip.end_time)
    return {"message": "Delivery trip created successfully", "data": {"id": db_trip.id}}

@router.get("/total_worked_time/")
async def get_total_worked_time(user_id: int, start: datetime, end: datetime, session: AsyncSession = Depends(get_db)):
    calculator = TimeCalculator(session)
    result = await calculator.calculate_work_time(user_id, start, end)
    return result

@router.get("/work_shifts/")
async def get_all_work_shifts(session: AsyncSession = Depends(get_db)):
    work_shifts = await session.query(WorkShift).all()
    return {"data": work_shifts}

@router.get("/abreaks/")
async def get_all_abreaks(session: AsyncSession = Depends(get_db)):
    abreaks = await session.query(abreak).all()
    return {"data": abreaks}

@router.get("/delivery_trips/")
async def get_all_delivery_trips(session: AsyncSession = Depends(get_db)):
    delivery_trips = await session.query(DeliveryTrip).all()
    return {"data": delivery_trips}