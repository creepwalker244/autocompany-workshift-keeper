from pydantic import BaseModel
from datetime import datetime

class WorkShiftSchema(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime

class BreakSchema(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime

class DeliveryTripSchema(BaseModel):
    driver_id: int
    start_time: datetime
    end_time: datetime