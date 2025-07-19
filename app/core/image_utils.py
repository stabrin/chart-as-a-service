# app/core/image_utils.py

from PIL import Image, ImageDraw, ImageFont
import io

def add_watermark(image_bytes: bytes, text: str) -> bytes:
    """
    Добавляет текстовый водяной знак в правый нижний угол изображения.
    """
    # Открываем основное изображение
    with Image.open(io.BytesIO(image_bytes)).convert("RGBA") as base:
        # Создаем прозрачный слой для текста такого же размера
        txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))

        # Выбираем шрифт (можно указать путь к своему .ttf файлу, если нужно)
        # Для простоты используем шрифт по умолчанию
        try:
            # Попытка загрузить стандартный шрифт
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            # Если шрифт не найден, используем шрифт по умолчанию
            font = ImageFont.load_default()

        # Получаем контекст для рисования на текстовом слое
        d = ImageDraw.Draw(txt_layer)

        # Вычисляем позицию для текста (правый нижний угол с отступом)
        text_bbox = d.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        width, height = base.size
        x = width - text_width - 15  # 15px отступ справа
        y = height - text_height - 15 # 15px отступ снизу

        # Рисуем текст на прозрачном слое с полупрозрачностью
        d.text((x, y), text, font=font, fill=(128, 128, 128, 100)) # Серый, полупрозрачный

        # Накладываем текстовый слой на основное изображение
        out = Image.alpha_composite(base, txt_layer)

        # Сохраняем результат в байтовый буфер
        buf = io.BytesIO()
        out.save(buf, format='PNG')
        buf.seek(0)
        
        return buf.getvalue()