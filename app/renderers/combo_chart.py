# app/renderers/combo_chart.py

import io
import matplotlib.pyplot as plt
from ..core.schemas import ChartData, ChartOptions, Dataset

plt.switch_backend('AGG')

def render(data: ChartData, options: ChartOptions) -> bytes:
    """
    Создает комбинированный график.
    
    ПРАВИЛО:
    - Первый набор данных (datasets[0]) рисуется как столбчатая диаграмма (bar).
    - Все последующие наборы данных рисуются как линейные графики (line).
    """
    if len(data.datasets) < 2:
        raise ValueError("Combo chart requires at least 2 datasets (1 for bars, 1+ for lines).")

    fig, ax = plt.subplots(figsize=options.figsize)

    # --- Рисуем столбцы (первый dataset) ---
    bar_dataset: Dataset = data.datasets[0]
    ax.bar(
        data.labels, 
        bar_dataset.data, 
        label=bar_dataset.label, 
        color=bar_dataset.color or '#add8e6' # Светло-голубой по умолчанию
    )
    ax.set_ylabel(bar_dataset.label or options.y_label, color=bar_dataset.color or 'blue')
    ax.tick_params(axis='y', labelcolor=bar_dataset.color or 'blue')


    # --- Рисуем линии (остальные datasets) ---
    # Создаем вторую ось Y, которая будет разделять ту же ось X
    ax2 = ax.twinx()

    line_datasets: list[Dataset] = data.datasets[1:]
    for i, dataset in enumerate(line_datasets):
        # Используем цвет из датасета или назначаем свой
        line_color = dataset.color or f'C{i+1}' # C1, C2 и т.д. - стандартные цвета matplotlib
        ax2.plot(
            data.labels, 
            dataset.data, 
            label=dataset.label, 
            color=line_color,
            marker='o'
        )
    
    # Настраиваем вторую ось Y
    # Для простоты возьмем лейбл от первого линейного графика
    ax2.set_ylabel(line_datasets[0].label, color=line_datasets[0].color or 'red')
    ax2.tick_params(axis='y', labelcolor=line_datasets[0].color or 'red')


    # --- Общие настройки ---
    ax.set_xlabel(options.x_label)
    if options.title:
        ax.set_title(options.title, fontsize=16)

    # Собираем легенды с обеих осей в одну
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    ax.grid(True, linestyle='--', alpha=0.6, axis='y') # Сетка только для основной оси
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