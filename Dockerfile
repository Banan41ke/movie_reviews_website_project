# 1. Базовый образ Python
FROM python:3.12-slim

# 2. Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Рабочая директория внутри контейнера
WORKDIR /app

# 4. Системные зависимости (для Pillow, psycopg и т.п.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Копируем зависимости
COPY requirements.txt .

# 6. Устанавливаем Python-зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# 7. Копируем ВЕСЬ проект
COPY . .

# 8. Открываем порт Django
EXPOSE 8000

# 9. Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
