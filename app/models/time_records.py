from sqlalchemy import Column, Integer, DateTime, func, and_, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from datetime import datetime

Base = declarative_base()
class WorkShift(Base):
    __tablename__ = "work_shifts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    @classmethod
    async def get_worked_seconds(cls, user_id: int, start: datetime, end: datetime, session: AsyncSession):
        stmt = select(
            func.coalesce(
                func.sum(
                    func.extract('epoch', cls.end_time - cls.start_time)
                ), 
                0
            )
        ).where(
            (cls.user_id == user_id) &
            (cls.start_time >= start) &
            (cls.end_time <= end)
        )
        
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def insert_work_shift(cls, session: AsyncSession, user_id: int, start_time: datetime, end_time: datetime):
        new_shift = cls(user_id=user_id, start_time=start_time, end_time=end_time)
        session.add(new_shift)
        await session.commit()
        return new_shift

class Break(Base):
    __tablename__ = "breaks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    @classmethod
    async def get_break_seconds(cls, user_id: int, start: datetime, end: datetime, session: AsyncSession):
        stmt = select(
            func.coalesce(
                func.sum(
                    func.extract('epoch', cls.end_time - cls.start_time)
                ),
                0
            )
        ).where(
            (cls.user_id == user_id) &
            (cls.start_time >= start) &
            (cls.end_time <= end)
        )
        
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def insert_break(cls, session: AsyncSession, user_id: int, start_time: datetime, end_time: datetime):
        new_break = cls(user_id=user_id, start_time=start_time, end_time=end_time)
        session.add(new_break)
        await session.commit()
        return new_break

class DeliveryTrip(Base):
    __tablename__ = "delivery_trips"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    @classmethod
    async def get_delivery_seconds(cls, driver_id: int, start: datetime, end: datetime, session: AsyncSession):
        result = await session.query(func.extract('epoch', cls.end_time - cls.start_time).label('seconds')).\
            filter(and_(cls.driver_id == driver_id, cls.start_time >= start, cls.end_time <= end)).\
            correlate()
        return await result.scalar() or 0

    @classmethod
    async def insert_delivery_trip(cls, session: AsyncSession, driver_id: int, start_time: datetime, end_time: datetime):
        new_trip = cls(driver_id=driver_id, start_time=start_time, end_time=end_time)
        session.add(new_trip)
        await session.commit()
        return new_trip