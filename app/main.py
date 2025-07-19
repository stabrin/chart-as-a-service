# app/main.py

from fastapi import FastAPI, Body, Response, Depends, Query 
from fastapi.security.api_key import APIKey
from pydantic import BaseModel, Field
from typing import List
import json

from .core.schemas import ChartRequest
from .core.chart_factory import create_chart
from .core.image_utils import add_watermark
from .core.auth import get_api_key 
from .core.telegram_sender import send_photo_to_telegram

app = FastAPI(
    title="Chart-as-a-Service",
    description="API для генерации графиков на лету.",
    version="1.0.0"
)

@app.post("/generate_chart")
async def generate_chart(
    request: ChartRequest = Body(...),
    api_key: APIKey = Depends(get_api_key)
):
    try:
        # 1. Генерируем график
        chart_bytes = create_chart(request)
        
        # 2. Добавляем водяной знак
        final_image_bytes = add_watermark(chart_bytes, text="@TabrinSergey")

        # 3. Возвращаем результат
        return Response(content=final_image_bytes, media_type="image/png")
    
    except ValueError as e:
        return Response(content=str(e), status_code=400)

class TelegramSendRequest(BaseModel):
    chart_request: ChartRequest
    chat_ids: List[str]
    bot_token: str  # <-- Добавлено обязательное поле
    caption: str = ""

@app.post("/generate_and_send_to_telegram", dependencies=[Depends(get_api_key)])
async def generate_and_send(request: TelegramSendRequest):
    try:
        # 1. Генерируем график
        chart_bytes = create_chart(request.chart_request)
        final_image_bytes = add_watermark(chart_bytes, text="@IT-Workshop")

        # 2. Отправляем всем получателям, передавая токен
        for chat_id in request.chat_ids:
            await send_photo_to_telegram(
                bot_token=request.bot_token, # <-- Передаем токен
                chat_id=chat_id,
                image_bytes=final_image_bytes,
                caption=request.caption
            )
        
        return {"status": "ok", "message": f"Sent to {len(request.chat_ids)} chats."}

    except Exception as e:
        # Ошибки генерации графика
        return Response(content=str(e), status_code=400)
    except Exception as e:
        # Ошибки отправки в телеграм или другие
        print(f"An error occurred: {e}")
        return Response(content=f"An internal error occurred: {e}", status_code=500)

@app.get("/generate_and_send_get", dependencies=[Depends(get_api_key)])
async def generate_and_send_from_get(
    # Мы будем принимать JSON-объект как одну большую строку
    chart_request_str: str = Query(alias="chart_request"),
    chat_ids_str: str = Query(alias="chat_ids"), # Список ID как строка "id1,id2,id3"
    bot_token: str = Query(alias="bot_token"),
    caption: str = Query(alias="caption", default="")
):
    try:
        # 1. Парсим строки обратно в Python-объекты
        chart_request_dict = json.loads(chart_request_str)
        chart_request = ChartRequest(**chart_request_dict)
        chat_ids = chat_ids_str.split(',')

        # 2. Генерируем график
        chart_bytes = create_chart(chart_request)
        final_image_bytes = add_watermark(chart_bytes, text="@IT-Workshop")

        # 3. Отправляем в Telegram
        for chat_id in chat_ids:
            # Убираем пробелы, если они есть
            clean_chat_id = chat_id.strip()
            if clean_chat_id:
                await send_photo_to_telegram(
                    bot_token=bot_token,
                    chat_id=clean_chat_id,
                    image_bytes=final_image_bytes,
                    caption=caption
                )
        
        # Для Qlik Load From мы должны вернуть какой-то ответ, чтобы он не упал
        return {"status": "ok", "message": f"Sent to {len(chat_ids)} chats."}

    except json.JSONDecodeError:
        return Response(content="Invalid JSON format in 'chart_request' parameter.", status_code=400)
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response(content=f"An internal error occurred: {e}", status_code=500)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Chart-as-a-Service is running!"}