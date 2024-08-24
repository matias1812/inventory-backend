import matplotlib.pyplot as plt
import io
import base64

def generar_grafico(tipo, datos, titulo, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    if tipo == 'bar':
        plt.bar(datos['x'], datos['y'])
    elif tipo == 'line':
        plt.plot(datos['x'], datos['y'])
    # Añade más tipos según sea necesario
    
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    
    return base64.b64encode(img.getvalue()).decode()
