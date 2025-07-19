# app/main.py

from fastapi import FastAPI, Body, Response, Depends
from fastapi.security.api_key import APIKey

from .core.schemas import ChartRequest
from .core.chart_factory import create_chart
from .core.image_utils import add_watermark
from .core.auth import get_api_key # <-- 1. Импортируем нашу зависимость

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


@app.get("/")
async def root():
    return {"status": "ok", "message": "Chart-as-a-Service is running!"}