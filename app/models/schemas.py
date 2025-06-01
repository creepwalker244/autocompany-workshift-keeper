from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import Field


class WorkShiftSchema(BaseModel):
    user_id: int = Field(..., example=1)
    start_time: datetime = Field(..., example="2024-01-01T09:00:00")
    end_time: datetime = Field(..., example="2024-01-01T18:00:00")

class BreakSchema(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime

class DeliveryTripSchema(BaseModel):
    driver_id: int
    start_time: datetime
    end_time: datetime
    

class UserAuth(BaseModel):
    username: str
    password: str

class UserRegister(UserAuth):
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenResponse(Token):
    pass

class TokenData(BaseModel):
    username: str | None = None

# Модель для ответа с данными пользователя
class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy моделями