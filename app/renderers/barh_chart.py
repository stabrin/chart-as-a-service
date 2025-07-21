# app/renderers/barh_chart.py

import io
import matplotlib.pyplot as plt
from ..core.schemas import ChartData, ChartOptions

plt.switch_backend('AGG')

def render(data: ChartData, options: ChartOptions) -> bytes:
    if not data.datasets:
        raise ValueError("Cannot render bar chart with no datasets.")
    
    # --- НАЧАЛО ИЗМЕНЕНИЙ: ЛОГИКА ДЛЯ ВЛОЖЕННЫХ ПОЛОС ---
    
    # Основной набор данных (синяя полоса)
    total_dataset = data.datasets[0]
    
    # Проверяем, есть ли второй, вложенный набор данных (зеленая полоса)
    ai_dataset = data.datasets[1] if len(data.datasets) > 1 else None

    if len(data.labels) != len(total_dataset.data):
        raise ValueError(
            f"Shape mismatch: {len(data.labels)} labels and {len(total_dataset.data)} data points."
        )

    fig, ax = plt.subplots(figsize=options.figsize)

    bar_height = options.bar_height if options.bar_height is not None else 0.6

    # 1. Рисуем основную (синюю) полосу
    bars = ax.barh(
        data.labels, 
        total_dataset.data, 
        color='#3470a3',  # Насыщенный синий
        height=bar_height,
        label=total_dataset.label or 'Всего'
    )

    # 2. Если есть данные для АИ, рисуем вложенную (зеленую) полосу поверх
    if ai_dataset:
        ax.barh(
            data.labels,
            ai_dataset.data,
            color='#4CAF50',  # Приятный зеленый
            height=bar_height, # Та же высота, чтобы полностью перекрывать часть синей
            label=ai_dataset.label or 'АИ'
        )

    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    ax.invert_yaxis()

    if options.title:
        ax.set_title(options.title, fontsize=16, pad=20)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', colors='#a0a0a0')
    ax.spines['bottom'].set_color('#a0a0a0')

    # Добавляем значения в конце ОСНОВНОЙ (синей) полосы
    for i, bar in enumerate(bars):
        # Используем значение из total_dataset, чтобы всегда показывать общий итог
        width = total_dataset.data[i]
        if width > 0:
            ax.text(
                width + (ax.get_xlim()[1] * 0.01),
                bar.get_y() + bar.get_height() / 2,
                f'{int(width)}',
                ha='left',
                va='center',
                fontsize=9,
                color='#333333'
            )
    
    plt.xlim(right=ax.get_xlim()[1] * 1.18)
    plt.tight_layout(pad=1.5)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    plt.close(fig)

    return image_bytes