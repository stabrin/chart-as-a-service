# 1. Используем официальный образ Python
FROM python:3.9-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Устанавливаем системные зависимости, необходимые для Matplotlib
# fontconfig нужен для работы со шрифтами (особенно с кириллицей)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# 4. Копируем файл с зависимостями
COPY requirements.txt .

# 5. Устанавливаем Python-зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Копируем код приложения.
# Это происходит при сборке образа. Для разработки мы используем volume,
# но это нужно для production-сборки.
COPY ./app /app

# Команда по умолчанию (будет переопределена в docker-compose для разработки)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]