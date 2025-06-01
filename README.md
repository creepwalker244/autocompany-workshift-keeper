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

4. доступные методы в свагере: https://127.0.0.1:8000/docs