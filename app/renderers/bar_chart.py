# app/renderers/bar_chart.py

import io
import matplotlib.pyplot as plt
from ..core.schemas import ChartData, ChartOptions

# Отключаем интерактивный режим Matplotlib, т.к. работаем на сервере
plt.switch_backend('AGG')

def render(data: ChartData, options: ChartOptions) -> bytes:
    """
    Создает столбчатую диаграмму на основе предоставленных данных и опций.
    Возвращает изображение в виде байтов (PNG).
    """
    if not data.datasets:
        raise ValueError("Cannot render bar chart with no datasets.")
    
    # Берем данные из первого набора данных
    first_dataset = data.datasets[0]
    values_to_plot = first_dataset.data
    # Используем цвет из набора данных, если он есть, иначе из общих опций
    colors_to_use = first_dataset.color or options.colors

    # Создаем фигуру и оси для графика, используя размер из опций
    fig, ax = plt.subplots(figsize=options.figsize)

    # Рисуем столбчатую диаграмму
    ax.bar(data.labels, values_to_plot, color=colors_to_use)

    # Применяем опции кастомизации, если они указаны
    if options.title:
        ax.set_title(options.title, fontsize=16)
    if options.x_label:
        ax.set_xlabel(options.x_label, fontsize=12)
    if options.y_label:
        ax.set_ylabel(options.y_label, fontsize=12)
    
    # Улучшаем отображение (например, поворачиваем подписи по оси X, если их много)
    if len(data.labels) > 5:
        plt.xticks(rotation=45, ha="right")

    # Убеждаемся, что все элементы помещаются на холст
    plt.tight_layout()

    # Сохраняем график в буфер в памяти вместо файла на диске
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    
    # "Перематываем" буфер в начало, чтобы его можно было прочитать
    buf.seek(0)
    
    # Получаем байты из буфера
    image_bytes = buf.getvalue()
    
    # Закрываем буфер и фигуру, чтобы освободить память
    buf.close()
    plt.close(fig)

    return image_bytes