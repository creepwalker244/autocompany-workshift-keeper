from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.users import User
from app.models.schemas import UserAuth, UserRegister, TokenResponse, UserResponse
from app.services.security import verify_password, get_password_hash, create_access_token, get_current_active_user
from app.services.db_init import get_db
from datetime import timedelta 

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES=10

@router.post(
    "/register",
    response_model=TokenResponse,
    tags=["Authentication"],
    summary="Регистрация нового пользователя",
    responses={
        200: {
            "description": "Успешная регистрация",
            "content": {
                "application/json": {
                    "example": {"access_token": "jwt.token.here", "token_type": "bearer"}
                }
            }
        },
        400: {"description": "Пользователь уже существует"}
    }
)
async def register(user: UserRegister, db: Session = Depends(get_db)):
     # Проверяем существование пользователя
    existing_user = await db.execute(select(User).where(User.username == user.username))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Создаем нового пользователя
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        full_name=user.full_name,
        password=hashed_password
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # Создаем токен
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=TokenResponse)
async def login(user: UserAuth, db: Session = Depends(get_db)):
    # Ищем пользователя
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Генерируем токен
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)  # Используем Pydantic модель для ответа
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user