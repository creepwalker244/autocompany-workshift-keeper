from sqlalchemy import func, extract, case, and_

class WorkShift(Base):
    """
    WorkShift model - модель для хранения рабочих часов
    """
    
    @classmethod
    def get_worked_seconds(cls, user_id: int, start: datetime, end: datetime):
        return (
            select(
                func.sum(
                    func.extract('epoch', cls.end_time - cls.start_time)
                ).filter(
                    and_(
                        cls.user_id == user_id,
                        cls.start_time >= start,
                        cls.end_time <= end
                    )
                )
            )
        )

class Break(Base):
    """
        класс перерывов
    """
    @classmethod
    def get_break_seconds(cls, user_id: int, start: datetime, end: datetime):
        return (
            select(
                func.sum(
                    func.extract('epoch', cls.end_time - cls.start_time)
                ).filter(
                    and_(
                        cls.user_id == user_id,
                        cls.start_time >= start,
                        cls.end_time <= end
                    )
                )
            )
        )

class DeliveryTrip(Base):
    """
    DeliveryTrip model - модель для хранения данных о доставках
    """
    @classmethod
    def get_delivery_seconds(cls, user_id: int, start: datetime, end: datetime):
        return (
            select(
                func.sum(
                    func.extract('epoch', cls.end_time - cls.start_time)
                ).filter(
                    and_(
                        cls.driver_id == user_id,
                        cls.start_time >= start,
                        cls.end_time <= end
                    )
                )
            )
        )