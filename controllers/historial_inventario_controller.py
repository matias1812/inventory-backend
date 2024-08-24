from flask import request, jsonify
from models.historial_inventario import HistorialInventario
from app import db

def registrar_historial():
    data = request.json
    nuevo_historial = HistorialInventario(
        inventario_id=data['inventario_id'],
        cambio_stock=data['cambio_stock'],
        tipo_cambio=data['tipo_cambio'],
        usuario_id=data['usuario_id']
    )
    db.session.add(nuevo_historial)
    db.session.commit()
    return jsonify({"mensaje": "Historial registrado exitosamente"}), 201

def obtener_historiales():
    historiales = HistorialInventario.query.all()
    return jsonify([historial.as_dict() for historial in historiales]), 200

def obtener_historial(historial_id):
    historial = HistorialInventario.query.get(historial_id)
    if historial:
        return jsonify(historial.as_dict()), 200
    return jsonify({"error": "Historial no encontrado"}), 404

def actualizar_historial(historial_id):
    data = request.json
    historial = HistorialInventario.query.get(historial_id)
    if historial:
        historial.inventario_id = data['inventario_id']
        historial.cambio_stock = data['cambio_stock']
        historial.tipo_cambio = data['tipo_cambio']
        historial.usuario_id = data['usuario_id']
        db.session.commit()
        return jsonify({"mensaje": "Historial actualizado exitosamente"}), 200
    return jsonify({"error": "Historial no encontrado"}), 404

def eliminar_historial(historial_id):
    historial = HistorialInventario.query.get(historial_id)
    if historial:
        db.session.delete(historial)
        db.session.commit()
        return jsonify({"mensaje": "Historial eliminado exitosamente"}), 200
    return jsonify({"error": "Historial no encontrado"}), 404
