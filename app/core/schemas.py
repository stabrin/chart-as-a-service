# app/core/schemas.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# НОВАЯ модель: описывает один набор данных (например, одна линия на графике)
class Dataset(BaseModel):
    label: str  # Название этого набора данных (для легенды)
    data: List[float]
    # Цвет можно указать для конкретного набора данных
    color: Optional[str] = None

# ОБНОВЛЕННАЯ модель для данных графика
class ChartData(BaseModel):
    labels: List[str]  # Это общие метки по оси X
    datasets: List[Dataset] # Теперь это список наборов данных

# Модель опций остается прежней
class ChartOptions(BaseModel):
    title: Optional[str] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    # Это поле станет менее используемым, т.к. цвета можно задавать в Dataset
    colors: Optional[List[str]] = None
    figsize: Optional[List[int]] = [10, 6]

# Основная модель запроса остается прежней
class ChartRequest(BaseModel):
    chart_type: str = Field(..., description="Тип графика (например, 'bar', 'line')")
    data: ChartData
    options: Optional[ChartOptions] = ChartOptions()