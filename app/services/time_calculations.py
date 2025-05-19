from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WorkShift, Break, DeliveryTrip

class TimeCalculator:
    """ Класс для расчета времени работы сотрудника """
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def calculate_work_time(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """ Расчет времени работы сотрудника """
        total_worked = await self._execute_scalar(
            WorkShift.get_worked_seconds(user_id, start_date, end_date)
        )
        
        total_breaks = await self._execute_scalar(
            Break.get_break_seconds(user_id, start_date, end_date)
        )
        
        total_deliveries = await self._execute_scalar(
            DeliveryTrip.get_delivery_seconds(user_id, start_date, end_date)
        )
        
        clean_work = max(total_worked - total_breaks, 0)
        
        """возвращает словарь с информацией о работе сотрудника
            в формате ключ : значение
        """
        return {
            "total_worked_hours": self.seconds_to_hours(total_worked),
            "clean_work_hours": self.seconds_to_hours(clean_work),
            "delivery_hours": self.seconds_to_hours(total_deliveries)
        }
        
    async def _execute_scalar(self, query):
        """ Выполняет запрос и возвращает результат в виде int """
        result = await self.session.execute(query)
        return result.scalar() or 0
        
    @staticmethod
    def seconds_to_hours(seconds: int) -> float:
            
        return round(seconds / 3600, 2) if seconds else 0.0