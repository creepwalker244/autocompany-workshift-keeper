import os
import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.app import app  # Убедитесь что app импортируется правильно
from app.models.users import User, Role
from app.services.security import get_password_hash

# Конфигурация
BASE_URL = "http://localhost:8000"
TEST_DB_URL = os.getenv("TEST_DB_URL", "sqlite+aiosqlite:///./test.db")

@pytest.fixture(scope="module")
async def engine():
    engine = create_async_engine(TEST_DB_URL)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSession(engine) as session:
        # Создаем тестовых пользователей
        test_users = [
            User(
                username="regular_user",
                password=get_password_hash("userpass"),
                role=Role.USER,
                full_name="Test User",
                is_active=True
            ),
            User(
                username="admin_user",
                password=get_password_hash("adminpass"),
                role=Role.ADMIN,
                full_name="Test Admin",
                is_active=True
            )
        ]
        
        session.add_all(test_users)
        await session.commit()
        yield session
        await session.rollback()

@pytest.fixture(scope="module")
async def client():
    # Правильное создание AsyncClient
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        yield client

@pytest.mark.asyncio
async def test_auth_flow(client, session):
    # Тест регистрации
    response = await client.post(
        "/auth/register",
        json={
            "username": "new_user",
            "password": "newpass",
            "full_name": "New User"
        }
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_work_shift_operations(client, session):
    # Получаем токен админа
    response = await client.post(
        "/auth/token",
        data={"username": "admin_user", "password": "adminpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Создание рабочей смены
    work_shift = {
        "user_id": 1,
        "start_time": "2024-01-01T09:00:00",
        "end_time": "2024-01-01T17:00:00"
    }
    
    response = await client.post(
        "/work/work_shifts/",
        json=work_shift,
        headers=headers
    )
    assert response.status_code == 200
    assert "id" in response.json()