# app/renderers/barh_chart.py - ФИНАЛЬНАЯ ВЕРСИЯ

import io
import matplotlib.pyplot as plt
import numpy as np
from ..core.schemas import ChartData, ChartOptions

plt.switch_backend('AGG')

def render(data: ChartData, options: ChartOptions) -> bytes:
    if not data.datasets:
        raise ValueError("Cannot render bar chart with no datasets.")
    
    total_dataset = data.datasets[0]
    ai_dataset = data.datasets[1] if len(data.datasets) > 1 else None

    if len(data.labels) != len(total_dataset.data):
        raise ValueError(f"Shape mismatch: {len(data.labels)} labels and {len(total_dataset.data)} data points.")

    fig, ax = plt.subplots(figsize=options.figsize)
    bar_height = options.bar_height if options.bar_height is not None else 0.6
    y_pos = np.arange(len(data.labels))

    bars = ax.barh(y_pos, total_dataset.data, color='#3470a3', height=bar_height, label=total_dataset.label or 'Всего')

    if ai_dataset:
        ai_bar_height = bar_height * 0.5
        ax.barh(y_pos, ai_dataset.data, color='#4CAF50', height=ai_bar_height, align='center', label=ai_dataset.label or 'АИ')

    ax.set_yticks(y_pos, labels=data.labels)
    ax.legend(loc='lower right', frameon=False, ncol=2)
    ax.invert_yaxis()

    if options.title:
        ax.set_title(options.title, fontsize=16, pad=20)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', colors='#a0a0a0')
    ax.spines['bottom'].set_color('#a0a0a0')

    # Блок, который рисует ОБА значения
    for i, bar in enumerate(bars):
        total_width = total_dataset.data[i]
        
        if total_width > 0:
            ax.text(
                total_width + (ax.get_xlim()[1] * 0.01), bar.get_y() + bar.get_height() / 2,
                f'{int(total_width)}', ha='left', va='center', fontsize=9, color='#333333'
            )
            
        if ai_dataset and len(ai_dataset.data) > i:
            ai_width = ai_dataset.data[i]
            if ai_width > 0:
                ax.text(
                    ai_width - (ax.get_xlim()[1] * 0.005), bar.get_y() + bar.get_height() / 2,
                    f'{int(ai_width)}', ha='right', va='center', fontsize=8, color='white', weight='bold'
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