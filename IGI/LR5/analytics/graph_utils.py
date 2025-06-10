import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from typing import List, Dict, Tuple, Any
import numpy as np

def generate_line_chart(labels: List[str],
                       datasets: List[Dict[str, Any]],
                       title: str = '',
                       xlabel: str = '',
                       ylabel: str = '') -> str:
    """Generate a line chart and return it as a base64 encoded string."""
    plt.figure(figsize=(8, 5))

    for dataset in datasets:
        plt.plot(labels, dataset['data'], label=dataset['label'])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    plt.close()

    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64

def generate_pie_chart(labels: List[str],
                      data: List[float],
                      title: str = '') -> str:
    """Generate a pie chart and return it as a base64 encoded string."""
    plt.figure(figsize=(6, 6))

    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    plt.close()

    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64

def generate_bar_chart(labels: List[str],
                      data: List[float],
                      title: str = '',
                      xlabel: str = '',
                      ylabel: str = '') -> str:
    """Generate a bar chart and return it as a base64 encoded string."""
    plt.figure(figsize=(8, 5))

    plt.bar(labels, data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    plt.close()

    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64
