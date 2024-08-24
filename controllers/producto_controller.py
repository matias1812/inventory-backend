from flask import request, jsonify
from models.producto import Producto
from models.movimiento import Movimiento
from app import db

def registrar_producto():
    data = request.json
    nuevo_producto = Producto(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        unidad_medida=data['unidad_medida'],
        status=data['status'],
        ubicacion=data['ubicacion']
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    
    # Registrar movimiento
    movimiento = Movimiento(
        operacion='registro',
        producto_id=nuevo_producto.id,
        usuario_id=data['usuario_id'],
        tipo='entrada',
        cantidad=data['cantidad']  # Suponiendo que se agregue una cantidad inicial
    )
    db.session.add(movimiento)
    db.session.commit()

    return jsonify({"mensaje": "Producto registrado exitosamente"}), 201

def obtener_productos():
    productos = Producto.query.all()
    return jsonify([producto.as_dict() for producto in productos]), 200

def obtener_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if producto:
        return jsonify(producto.as_dict()), 200
    return jsonify({"error": "Producto no encontrado"}), 404

def actualizar_producto(producto_id):
    data = request.json
    producto = Producto.query.get(producto_id)
    
    if producto:
        # Actualizar Producto (solo los campos permitidos)
        if 'nombre' in data:
            producto.nombre = data['nombre']
        if 'descripcion' in data:
            producto.descripcion = data['descripcion']
        if 'ubicacion' in data:
            producto.ubicacion = data['ubicacion']
        if 'status' in data:
            producto.status = data['status']
                
        # Guardar los cambios
        db.session.commit()
        return jsonify({"mensaje": "Producto actualizado exitosamente"}), 200

    return jsonify({"error": "Producto no encontrado"}), 404  

def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if producto:
        # Obtener información antes de eliminar
        movimiento = Movimiento(
            operacion='eliminacion',
            producto_id=producto.id,
            usuario_id=request.json.get('usuario_id'),
            tipo='salida',  # O según sea el caso
            cantidad=0  # Si no se afecta cantidad, sino calcularlo
        )
        db.session.delete(producto)
        db.session.commit()

        # Registrar movimiento
        db.session.add(movimiento)
        db.session.commit()

        return jsonify({"mensaje": "Producto eliminado exitosamente"}), 200
    return jsonify({"error": "Producto no encontrado"}), 404
