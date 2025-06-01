# WorkShift Keeper API

Микросервис для учета рабочего времени сотрудников и контроля доставок

## 🛠 Технологический стек
- **Backend**: Python + FastAPI
- **База данных**: PostgreSQL + SQLAlchemy ORM
- **Аутентификация**: JWT-токены
- **Документация**: Swagger/OpenAPI 3.0
- **Валидация**: Pydantic


### Требования
- Python 3.10+
- PostgreSQL 12+
- Установленные зависимости: `pip install -r requirements.txt`

### Запуск
1. Создать виртуальное окружение:
```bash
python -m venv .venv && source .venv/bin/activate  # Linux/MacOS
python -m venv .venv && .venv\Scripts\activate     # Windows
```
2. Установить зависимости:
```bash
pip install -r requirements.txt
```
3. Запустить веб сервер:
```bash
uvicorn app.app:app --reload
```

4. Документация API
Доступна после запуска сервера:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

5. Ключевые методы API
Аутентификация
POST /auth/register - Регистрация пользователя

POST /auth/token - Получение JWT-токена

Рабочие смены
POST /work/work_shifts/ - Добавить смену (только для админов)

GET /work/total_worked_time/ - Получить суммарное время работы

Перерывы и доставки
POST /work/breaks/ - Зарегистрировать перерыв

POST /work/delivery_trips/ - Добавить доставку

7. Конфигурация
Создайте файл .env в корне проекта:

DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your-secret-key
