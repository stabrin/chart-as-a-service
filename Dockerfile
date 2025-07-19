# 1. Используем официальный образ Python
FROM python:3.9-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# 4. Копируем ТОЛЬКО файл с зависимостями
# Это лучший способ использовать кеш Docker. Этот слой пересобирается,
# только если requirements.txt изменился.
COPY requirements.txt .

# 5. Устанавливаем Python-зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Копируем ВЕСЬ остальной код проекта.
# Теперь структура внутри контейнера будет /app/app/main.py, что правильно.
COPY . .

# 7. Команда по умолчанию. Теперь она будет работать, т.к. структура верная.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]