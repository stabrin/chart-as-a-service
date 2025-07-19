# app/core/telegram_sender.py
import aiohttp
from typing import Optional

# Глобальные переменные с токеном убраны

async def send_photo_to_telegram(
    bot_token: str, # <-- Добавлен обязательный аргумент
    chat_id: str,
    image_bytes: bytes,
    caption: Optional[str] = None
):
    """
    Асинхронно отправляет изображение в указанный чат Telegram, используя предоставленный токен.
    """
    # URL формируется динамически на основе токена
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    data = aiohttp.FormData()
    data.add_field('chat_id', chat_id)
    data.add_field('photo', image_bytes, filename='chart.png', content_type='image/png')
    
    if caption:
        data.add_field('caption', caption)
        data.add_field('parse_mode', 'HTML')

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status != 200:
                response_text = await response.text()
                print(f"Failed to send photo to Telegram. Status: {response.status}, Response: {response_text}")
            response.raise_for_status()