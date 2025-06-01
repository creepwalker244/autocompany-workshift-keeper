from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="WorkShift Keeper API",
    description="API для учета рабочего времени сотрудников",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Эндпоинты для регистрации и аутентификации"
        },
        {
            "name": "Work",
            "description": "Операции с рабочим временем и доставками"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes.routes import router
from app.routes.auth import router as auth_router
#app.include_router(router)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(router, prefix="/work", tags=["Work"])
