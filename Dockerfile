# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей
COPY app/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Открываем порт, на котором работает приложение
EXPOSE 8000

# ОБЪЯВЛЯЕМ
ENV DATABASE_URL=${DATABASE_URL}

# Запускаем приложение
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
