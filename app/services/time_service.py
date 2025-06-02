from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.time_records import WorkShift, Break, DeliveryTrip

class TimeCalculator:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def calculate_work_time(self, user_id: int, start: datetime, end: datetime):
        # Рабочее время
        work_seconds = await WorkShift.get_worked_seconds(
            user_id, start, end, self.session
        )

        # Перерывы
        break_seconds = await Break.get_break_seconds(
            user_id, start, end, self.session
        )

        return {
            "total_worked_seconds": work_seconds - break_seconds,
            "work_seconds": work_seconds,
            "break_seconds": break_seconds
        }
        
    async def _execute_scalar(self, query):
        result = await self.session.execute(query)
        return await result.scalar() or 0
        
    @staticmethod
    def seconds_to_hours(seconds: int) -> float:
        return round(seconds / 3600, 2) if seconds else 0.0