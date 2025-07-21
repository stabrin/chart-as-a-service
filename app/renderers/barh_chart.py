# app/renderers/barh_chart.py

import io
import matplotlib.pyplot as plt
from ..core.schemas import ChartData, ChartOptions

plt.switch_backend('AGG')

def render(data: ChartData, options: ChartOptions) -> bytes:
    if not data.datasets:
        raise ValueError("Cannot render bar chart with no datasets.")
    
    first_dataset = data.datasets[0]
    values_to_plot = first_dataset.data
    colors_to_use = first_dataset.color or options.colors

    fig, ax = plt.subplots(figsize=options.figsize)

    # --- ИЗМЕНЕНИЕ 1: Используем новую опцию толщины полос ---
    # Если опция не передана, используем значение 0.6 по умолчанию
    bar_height = options.bar_height if options.bar_height is not None else 0.6
    bars = ax.barh(data.labels, values_to_plot, color=colors_to_use, height=bar_height)
    # --- КОНЕЦ ИЗМЕНЕНИЯ 1 ---

    if options.title:
        ax.set_title(options.title, fontsize=16, pad=20)
    if options.x_label:
        ax.set_xlabel(options.y_label, fontsize=12) 
    if options.y_label:
        ax.set_ylabel(options.x_label, fontsize=12)

    ax.invert_yaxis()
    ax.margins(y=0.01)

    # Убираем рамку для более чистого вида
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # --- ИЗМЕНЕНИЕ 2: Добавляем значения в конце каждой полосы ---
    for bar in bars:
        width = bar.get_width()
        # Размещаем текст. `bar.get_y() + bar.get_height() / 2` - это центр полосы по вертикали.
        # `width + width * 0.01` - небольшой отступ от конца полосы.
        ax.text(width + width * 0.01, 
                bar.get_y() + bar.get_height() / 2,
                f'{int(width)}', # Отображаем как целое число
                ha='left', 
                va='center')
    
    # Расширяем правую границу, чтобы текст точно поместился
    plt.xlim(right=ax.get_xlim()[1] * 1.1)
    # --- КОНЕЦ ИЗМЕНЕНИЯ 2 ---

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    plt.close(fig)

    return image_bytes