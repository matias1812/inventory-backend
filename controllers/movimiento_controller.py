import os
from flask import request, jsonify, send_from_directory
from models.movimiento import Movimiento
from models.inventario import Inventario
from models.usuario import Usuario
from models.producto import Producto
from app import db
from utils.graph import generar_grafico
from PyPDF2 import PdfReader, errors
from sqlalchemy.orm import joinedload

# Ruta para guardar los informes
UPLOAD_FOLDER = 'uploads/informes'

# Asegúrate de que el directorio existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def registrar_movimiento():
    data = request.json
    nuevo_movimiento = Movimiento(
        inventario_id=data['inventario_id'],
        tipo=data['tipo'],
        cantidad=data['cantidad'],
        usuario_id=data['usuario_id']
    )
    db.session.add(nuevo_movimiento)
    db.session.commit()
    return jsonify({"mensaje": "Movimiento registrado exitosamente"}), 201

from flask import jsonify
from datetime import datetime

def obtener_movimientos():
    try:
        # Realizar la consulta
        query = db.session.query(
            Movimiento.id,
            Movimiento.fecha,
            Movimiento.tipo,
            Movimiento.cantidad,
            Usuario.nombre.label('usuario_nombre'),
            Producto.nombre.label('producto_nombre')
        ).outerjoin(Usuario, Movimiento.usuario_id == Usuario.id) \
         .outerjoin(Inventario, Movimiento.inventario_id == Inventario.id) \
         .outerjoin(Producto, Inventario.producto_id == Producto.id)

        # Ejecutar la consulta
        resultados = query.all()
        print("Resultados de la consulta:", resultados)  # Añade esta línea para depuración

        # Preparar la respuesta con los datos deseados
        movimientos_list = []
        for movimiento in resultados:
            movimiento_dict = {
                'id': movimiento[0],  # El primer valor en la tupla es el id
                'fecha': movimiento[1].strftime('%Y-%m-%d %H:%M:%S'),  # El segundo valor en la tupla es la fecha
                'tipo': movimiento[2],  # El tercer valor en la tupla es el tipo
                'cantidad': movimiento[3],  # El cuarto valor en la tupla es la cantidad
                'usuario': movimiento[4] ,  # El quinto valor en la tupla es el nombre del usuario
                'producto': movimiento[5]  # El sexto valor en la tupla es el nombre del producto
            }
            movimientos_list.append(movimiento_dict)

        return jsonify(movimientos_list), 200
    except Exception as e:
        print(f"Error al obtener movimientos: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
        
def obtener_movimiento(movimiento_id):
    movimiento = Movimiento.query.get(movimiento_id)
    if movimiento:
        return jsonify(movimiento.as_dict()), 200
    return jsonify({"error": "Movimiento no encontrado"}), 404

def actualizar_movimiento(movimiento_id):
    data = request.json
    movimiento = Movimiento.query.get(movimiento_id)
    if movimiento:
        movimiento.inventario_id = data['inventario_id']
        movimiento.tipo = data['tipo']
        movimiento.cantidad = data['cantidad']
        movimiento.usuario_id = data['usuario_id']
        db.session.commit()
        return jsonify({"mensaje": "Movimiento actualizado exitosamente"}), 200
    return jsonify({"error": "Movimiento no encontrado"}), 404

def eliminar_movimiento(movimiento_id):
    movimiento = Movimiento.query.get(movimiento_id)
    if movimiento:
        db.session.delete(movimiento)
        db.session.commit()
        return jsonify({"mensaje": "Movimiento eliminado exitosamente"}), 200
    return jsonify({"error": "Movimiento no encontrado"}), 404

def verificar_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            if len(reader.pages) > 0:
                print("El PDF es válido.")
                return True
            else:
                print("El PDF no tiene páginas.")
                return False
    except errors.PdfReadError:
        print("Error al leer el PDF. Está corrupto o no es un archivo PDF válido.")
        return False

def generar_nombre_archivo(base_name, folder):
    """Genera un nombre de archivo único en la carpeta dada"""
    index = 0
    while True:
        filename = f"{base_name}{index}.pdf"
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):
            return filename
        index += 1

def get_unique_filename(base_name, extension, folder=UPLOAD_FOLDER):
    """Genera un nombre de archivo único en el directorio especificado.
    
    Args:
        base_name (str): Nombre base del archivo (sin extensión).
        extension (str): Extensión del archivo (ej. 'pdf').
        folder (str): Directorio donde buscar archivos existentes (opcional).

    Returns:
        str: Nombre de archivo único.
    """
    counter = 1
    filename = f"{base_name}.{extension}"
    file_path = os.path.join(folder, filename)
    
    # Buscar archivos existentes y generar un nuevo nombre si es necesario
    while os.path.exists(file_path):
        filename = f"{base_name}{counter}.{extension}"
        file_path = os.path.join(folder, filename)
        counter += 1

    return filename

def reporte_movimientos():
    movimientos = Movimiento.query.options(
        joinedload(Movimiento.inventario).joinedload(Inventario.producto),
        joinedload(Movimiento.usuarios)
    ).all()

    fechas = [movimiento.fecha.strftime('%Y-%m-%d') for movimiento in movimientos]
    cantidades = [movimiento.cantidad for movimiento in movimientos]
    productos = [movimiento.inventario.producto.nombre for movimiento in movimientos]  # Corrección aquí
    usuarios = [movimiento.usuarios.nombre for movimiento in movimientos]

    datos = {
        'x': fechas,
        'y': cantidades,
        'productos': productos,
        'usuarios': usuarios
    }
    
    pdf_data = generar_grafico(
        tipo='line',
        datos=datos,
        titulo='Informe de Movimientos',
        xlabel='Fecha',
        ylabel='Cantidad'
    )
    
    filename = get_unique_filename('informe_movimientos', 'pdf')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    print(f"Saving file to: {file_path}")

    with open(file_path, 'wb') as f:
        f.write(pdf_data)
    
    if verificar_pdf(file_path):
        return jsonify({"file_path": file_path})
    else:
        return jsonify({"error": "El PDF generado está corrupto o vacío."}), 500

def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404
