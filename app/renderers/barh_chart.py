# app/renderers/barh_chart.py

import io
import matplotlib.pyplot as plt
from ..core.schemas import ChartData, ChartOptions

plt.switch_backend('AGG')

def render(data: ChartData, options: ChartOptions) -> bytes:
    """
    Создает ГОРИЗОНТАЛЬНУЮ столбчатую диаграмму.
    Возвращает изображение в виде байтов (PNG).
    """
    if not data.datasets:
        raise ValueError("Cannot render bar chart with no datasets.")
    
    first_dataset = data.datasets[0]
    values_to_plot = first_dataset.data
    colors_to_use = first_dataset.color or options.colors

    fig, ax = plt.subplots(figsize=options.figsize)

    # Используем ax.barh() для горизонтальной диаграммы.
    # Обрати внимание, что labels и values поменялись местами в аргументах.
    ax.barh(data.labels, values_to_plot, color=colors_to_use)

    if options.title:
        ax.set_title(options.title, fontsize=16)
    if options.x_label:
        # Для горизонтального графика X и Y метки меняются местами
        ax.set_xlabel(options.y_label, fontsize=12) 
    if options.y_label:
        ax.set_ylabel(options.x_label, fontsize=12)

    # Убираем лишние отступы, чтобы метки были ближе к осям
    ax.invert_yaxis()  # Чтобы первый элемент был наверху
    ax.margins(y=0.01) # Уменьшаем отступы по оси Y

    plt.tight_layout()

    # --- Код сохранения в буфер остается таким же ---
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True) # Добавим transparent=True для подложки
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    plt.close(fig)

    return image_bytes