import matplotlib
matplotlib.use('Agg')
import io
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def generar_grafico(tipo, datos, titulo, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(12, 8))  # Tamaño del gráfico ajustado para más detalles

    if tipo == 'line':
        ax.plot(datos['x'], datos['y'], marker='o', linestyle='-', color='b', label='Cantidad')  # Gráfico de línea
        for i, txt in enumerate(datos['productos']):
            ax.annotate(txt, (datos['x'][i], datos['y'][i]), textcoords="offset points", xytext=(0,10), ha='center')  # Añadir nombres de productos
    elif tipo == 'bar':
        bars = ax.bar(datos['x'], datos['y'], color='skyblue', edgecolor='black', label='Cantidad')  # Gráfico de barras
        for bar, producto in zip(bars, datos['productos']):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, producto, ha='center', va='bottom')  # Añadir nombres de productos
    else:
        raise ValueError("Tipo de gráfico no soportado. Usa 'line' o 'bar'.")

    ax.set_title(titulo, fontsize=16, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.legend()
    
    # Ajustar el formato de la fecha si es necesario
    if pd.api.types.is_datetime64_any_dtype(datos['x']):
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    
    pdf_stream = io.BytesIO()
    plt.savefig(pdf_stream, format='pdf')
    plt.close(fig)
    
    return pdf_stream.getvalue()
