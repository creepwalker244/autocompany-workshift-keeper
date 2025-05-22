from sqlalchemy import func, extract, case, and_, insert
from sqlalchemy.orm import sessionmaker, Session
import datetime

class WorkShift(Base):
    """класс для работы с таблицей фиксирвания рабочих часов"""
    __tablename__ = "work_shifts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    @classmethod
    def get_worked_seconds(cls, user_id: int, start: datetime, end: datetime):
        """"возвращает количество секунд, которые пользователь отработал в заданном интервале"""
        return (
            WorkShift.session.query(
                func.extract('epoch', cls.end_time - cls.start_time).label('seconds')
            )
            .filter(
                and_(
                    cls.user_id == user_id,
                    cls.start_time >= start,
                    cls.end_time <= end
                )
            )
            .correlate()
        )

    @classmethod
    def insert_work_shift(cls, db_session: Session, user_id: int, start_time: datetime, end_time: datetime):
        """вставляет запись в таблицу"""
        new_shift = cls(user_id=user_id, start_time=start_time, end_time=end_time)
        db_session.add(new_shift)
        db_session.commit()
        return new_shift

class Break(Base):
    """класс для работы с таблицей фиксирвания перерывов"""
    __tablename__ = "breaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    @classmethod
    def get_break_seconds(cls, user_id: int, start: datetime, end: datetime):
        """"возвращает количество секунд, которые были потрачены на перерыв"""
        return (
            Break.session.query(
                func.extract('epoch', cls.end_time - cls.start_time).label('seconds')
            )
            .filter(
                and_(
                    cls.user_id == user_id,
                    cls.start_time >= start,
                    cls.end_time <= end
                )
            )
            .correlate()
        )

    @classmethod
    def insert_break(cls, db_session: Session, user_id: int, start_time: datetime, end_time: datetime):
        """вставляет запись в таблицу"""
        new_break = cls(user_id=user_id, start_time=start_time, end_time=end_time)
        db_session.add(new_break)
        db_session.commit()
        return new_break

class DeliveryTrip(Base):
    """класс для работы с таблицей фиксирвания доставок"""
    __tablename__ = "delivery_trips"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    @classmethod
    def get_delivery_seconds(cls, driver_id: int, start: datetime, end: datetime):
        """"возвращает количество секунд, которые были потрачены на доставку"""
        return (
            DeliveryTrip.session.query(
                func.extract('epoch', cls.end_time - cls.start_time).label('seconds')
            )
            .filter(
                and_(
                    cls.driver_id == driver_id,
                    cls.start_time >= start,
                    cls.end_time <= end
                )
            )
            .correlate()
        )

    @classmethod
    def insert_delivery_trip(cls, db_session: Session, driver_id: int, start_time: datetime, end_time: datetime):
        """вставляет запись в таблицу"""
        new_trip = cls(driver_id=driver_id, start_time=start_time, end_time=end_time)
        db_session.add(new_trip)
        db_session.commit()
        return new_trip
