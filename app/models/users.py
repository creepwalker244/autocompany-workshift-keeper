from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime
import enum  # Добавляем импорт enum

Base = declarative_base()

# Используем enum.Enum для создания перечисления
class Role(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

role_enum = ENUM(
    Role,
    name="role",
    create_type=True,  # Автоматическое создание типа
    values_callable=lambda x: [e.value for e in x]
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    # Указываем Enum с типом Role и параметром name
    role = Column(role_enum, default=Role.USER)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    password = Column(String(60), nullable=False)