# app/renderers/line_chart.py

import io
import matplotlib.pyplot as plt
from ..core.schemas import ChartData, ChartOptions

plt.switch_backend('AGG')

def render(data: ChartData, options: ChartOptions) -> bytes:
    """
    Создает линейный график, поддерживающий несколько наборов данных.
    """
    fig, ax = plt.subplots(figsize=options.figsize)

    # Проходимся по каждому набору данных и рисуем его на графике
    for dataset in data.datasets:
        ax.plot(data.labels, dataset.data, label=dataset.label, color=dataset.color, marker='o')

    # Добавляем легенду, чтобы было понятно, какая линия что означает
    ax.legend()
    
    # Добавляем сетку для лучшей читаемости
    ax.grid(True, linestyle='--', alpha=0.6)

    # Применяем общие опции кастомизации
    if options.title:
        ax.set_title(options.title, fontsize=16)
    if options.x_label:
        ax.set_xlabel(options.x_label, fontsize=12)
    if options.y_label:
        ax.set_ylabel(options.y_label, fontsize=12)
    
    if len(data.labels) > 5:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    # Сохраняем в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    plt.close(fig)

    return image_bytes