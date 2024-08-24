from flask import request, jsonify, current_app, json, send_from_directory, abort
from werkzeug.utils import secure_filename
from models.contrato import Contrato
from models.inventario import Inventario
from app import db, app
import os
from datetime import datetime
from models.producto import Producto  # Asegúrate de que esta importación esté correcta
import traceback

def registrar_contrato():
    try:
        data = request.form
        productos_json = request.form.get('productos')
        productos = json.loads(productos_json)
        archivo = request.files['archivo']
        numero_contrato = data.get('numero_contrato')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        # Definir la ruta del directorio y crear el directorio si no existe
        directorio = '/Users/matiast./Desktop/akasa/inventory-backend/uploads'
        if not os.path.exists(directorio):
            os.makedirs(directorio)

        archivo_path = os.path.join(directorio, secure_filename(archivo.filename))
        archivo.save(archivo_path)

        contrato = Contrato(
            numero_contrato=numero_contrato,
            fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d'),
            fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d'),
            archivo_path=archivo_path
        )
        db.session.add(contrato)
        db.session.commit()

        for producto_data in productos:  # Cambiado de Productos a productos
            print(producto_data, "productos")
            nombre = producto_data.get('nombre')
            descripcion = producto_data.get('descripcion')
            unidad_medida = producto_data.get('unidad_medida')
            status = producto_data.get('status')
            stock_inicial = producto_data.get('stock_inicial')
            ubicacion = producto_data.get('ubicacion')

            if stock_inicial is None:
                raise ValueError("Falta el campo 'stock_inicial' en uno o más productos")

            # Crear el producto antes de agregar al inventario
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                unidad_medida=unidad_medida,
                status=status,
                ubicacion=ubicacion  # Proporcionar una ubicación predeterminada si es necesario
            )
            db.session.add(producto)
            db.session.commit()

            inventario = Inventario(
                producto_id=producto.id,
                contrato_id=contrato.id,
                stock_inicial=stock_inicial,
                stock_actual=stock_inicial  # Inicialmente el stock actual es igual al stock inicial
            )
            db.session.add(inventario)

        db.session.commit()

        return jsonify({"message": "Contrato y productos registrados exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


def obtener_contratos():
    contratos = Contrato.query.all()
    return jsonify([contrato.as_dict() for contrato in contratos]), 200

def obtener_contrato(contrato_id):
    contrato = Contrato.query.get(contrato_id)
    if contrato:
        return jsonify(contrato.as_dict()), 200
    return jsonify({"error": "Contrato no encontrado"}), 404

def actualizar_contrato(contrato_id):
    contrato = Contrato.query.get(contrato_id)
    if not contrato:
        return jsonify({'message': 'Contrato no encontrado'}), 404

    data = request.json
    contrato.numero_contrato = data.get('numero_contrato', contrato.numero_contrato)  # Usa 'numero_contrato'
    contrato.created_at = data.get('fecha_inicio', contrato.fecha_inicio)
    contrato.fecha_fin = data.get('fecha_fin', contrato.fecha_fin)

    db.session.commit()
    return jsonify({'message': 'Contrato actualizado correctamente'})   

def eliminar_contrato(contrato_id):
    contrato = Contrato.query.get(contrato_id)
    if contrato:
        db.session.delete(contrato)
        db.session.commit()
        return jsonify({"mensaje": "Contrato eliminado exitosamente"}), 200
    return jsonify({"error": "Contrato no encontrado"}), 404

def get_file(filename):
    uploads_dir = os.path.join(app.root_path, 'uploads')  # Combina el directorio raíz de la app con 'uploads'
    try:
        print(f"Attempting to send file: {os.path.join(uploads_dir, filename)}")  # Imprime la ruta completa del archivo
        return send_from_directory(uploads_dir, filename)
    except FileNotFoundError:
        print(f"File not found: {os.path.join(uploads_dir, filename)}")  # Imprime un mensaje si el archivo no se encuentra
        abort(404)