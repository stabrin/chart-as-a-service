# app/renderers/barh_chart.py

import io
import matplotlib.pyplot as plt
from ..core.schemas import ChartData, ChartOptions

plt.switch_backend('AGG')

def render(data: ChartData, options: ChartOptions) -> bytes:
    """
    Создает ГОРИЗОНТАЛЬНУЮ столбчатую диаграмму, отсортированную, с метками.
    """
    if not data.datasets:
        raise ValueError("Cannot render bar chart with no datasets.")
    
    first_dataset = data.datasets[0]
    
    # Проверяем, что количество меток и данных совпадает
    if len(data.labels) != len(first_dataset.data):
        raise ValueError(
            f"Shape mismatch: {len(data.labels)} labels and {len(first_dataset.data)} data points."
        )

    fig, ax = plt.subplots(figsize=options.figsize)

    bar_height = options.bar_height if options.bar_height is not None else 0.6
    bars = ax.barh(data.labels, first_dataset.data, color=options.colors, height=bar_height)

    ax.invert_yaxis()  # Верхний элемент из данных будет наверху графика

    if options.title:
        ax.set_title(options.title, fontsize=16, pad=20)
    
    # Убираем лишние элементы для чистоты
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True) # Оставим левую ось для наглядности
    ax.tick_params(axis='y', length=0) # Убираем черточки у меток по Y
    ax.tick_params(axis='x', colors='gray') # Делаем цифры по X серыми
    ax.spines['bottom'].set_color('gray')

    # Добавляем значения в конце каждой полосы
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width * 1.01,  # Небольшой отступ от конца полосы
            bar.get_y() + bar.get_height() / 2,
            f'{int(width)}',
            ha='left',
            va='center',
            fontsize=10,
            color='black'
        )
    
    # Автоматически расширяем правую границу, чтобы текст точно поместился
    plt.xlim(right=ax.get_xlim()[1] * 1.15)

    plt.tight_layout(pad=1.5)

    # Сохраняем в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    plt.close(fig)

    return image_bytes