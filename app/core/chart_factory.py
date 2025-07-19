# app/core/chart_factory.py

from .schemas import ChartRequest
from ..renderers import bar_chart, barh_chart, line_chart, combo_chart
from typing import Callable, Dict

# Словарь, который сопоставляет тип графика с функцией-рендерером
# Это легко расширять: добавили новый рендерер - добавили строчку сюда
RENDERERS: Dict[str, Callable] = {
    "bar": bar_chart.render,
    "barh": barh_chart.render,
    "line": line_chart.render,
    "combo": combo_chart.render,
    # "line": line_chart.render, # <- так мы добавим линейный график в будущем
}

def create_chart(request: ChartRequest) -> bytes:
    """
    Выбирает нужный рендерер на основе chart_type и генерирует график.
    """
    renderer_func = RENDERERS.get(request.chart_type.lower())

    if not renderer_func:
        # Если мы не нашли рендерер, выбрасываем ошибку.
        # FastAPI поймает ее и вернет клиенту ошибку 500.
        raise ValueError(f"Chart type '{request.chart_type}' is not supported.")
    
    # Вызываем найденную функцию (например, bar_chart.render)
    # и передаем в нее данные и опции из запроса
    return renderer_func(data=request.data, options=request.options)