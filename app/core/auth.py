# app/core/auth.py

import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# Получаем наш секретный ключ из переменных окружения.
# Если переменная не задана, сервис не должен стартовать, поэтому нет значения по умолчанию.
API_KEY = os.environ["API_KEY"]
API_KEY_NAME = "X-API-Key" # Так будет называться заголовок в запросе

# Создаем объект, который будет "искать" заголовок X-API-Key в запросах
api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    """
    Зависимость (dependency) для проверки API ключа.
    FastAPI будет автоматически вызывать эту функцию для каждого защищенного эндпоинта.
    """
    if not api_key_header:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key in header",
        )
    if api_key_header == API_KEY:
        # Ключ верный, возвращаем его. Запрос может продолжаться.
        return api_key_header
    else:
        # Ключ неверный, выбрасываем ошибку.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )