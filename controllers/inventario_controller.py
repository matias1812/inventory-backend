from flask import request, jsonify
from models.inventario import Inventario
from models.movimiento import Movimiento
from app import db

def registrar_inventario():
    data = request.json
    nuevo_inventario = Inventario(
        producto_id=data['producto_id'],
        contrato_id=data['contrato_id'],
        stock_inicial=data['stock_inicial'],
        stock_actual=data['stock_actual']
    )
    db.session.add(nuevo_inventario)
    db.session.commit()
    return jsonify({"mensaje": "Inventario registrado exitosamente"}), 201

def obtener_inventarios():
    try:
        inventarios = Inventario.query.all()
        inventarios_list = [inventario.as_dict() for inventario in inventarios]
        return jsonify(inventarios_list), 200
    except Exception as e:
        print(f"Error al obtener inventarios: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

def obtener_inventario(inventario_id):
    inventario = Inventario.query.get(inventario_id)
    if inventario:
        return jsonify(inventario.as_dict()), 200
    return jsonify({"error": "Inventario no encontrado"}), 404

def actualizar_inventario(inventario_id):
    data = request.json
    
    # Imprimir datos recibidos para depuración
    print("Datos recibidos:", data)
    
    inventario = Inventario.query.get(inventario_id)
    
    if inventario:
        # Verificar que los campos 'tipo' y 'cantidad' existan en los datos recibidos
        if 'tipo' not in data or 'cantidad' not in data:
            return jsonify({"error": "Tipo de movimiento o cantidad no especificados"}), 400
        
        # Verificar que la cantidad sea un número entero
        try:
            cantidad = int(data['cantidad'])
        except ValueError:
            return jsonify({"error": "Cantidad inválida"}), 400
        
        # Actualizar el stock basado en el tipo de movimiento
        if data['tipo'] == 'entrada':
            inventario.stock_actual += cantidad
        elif data['tipo'] == 'salida':
            # Asegurarse de que el stock no sea negativo
            if inventario.stock_actual >= cantidad:
                inventario.stock_actual -= cantidad
            else:
                return jsonify({"error": "Stock insuficiente para realizar la salida"}), 400
        else:
            return jsonify({"error": "Tipo de movimiento inválido"}), 400
        
        # Registrar el movimiento en la base de datos
        nuevo_movimiento = Movimiento(
            inventario_id=inventario_id,
            tipo=data['tipo'],
            cantidad=cantidad,
            usuario_id=data['usuario_id']  # Asegúrate de que 'usuario_id' esté en los datos recibidos
        )
        db.session.add(nuevo_movimiento)
        
        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        return jsonify({"mensaje": "Inventario actualizado exitosamente"}), 200
    
    # Retornar un error si el inventario no se encuentra
    return jsonify({"error": "Inventario no encontrado"}), 404

def eliminar_inventario(inventario_id, usuario_id):
    # Recuperar el inventario usando el inventario_id
    inventario = Inventario.query.get(inventario_id)
    
    if inventario:
        # Crear un nuevo movimiento con el stock actual
        nuevo_movimiento = Movimiento(
            inventario_id=inventario_id,
            tipo='salida',
            cantidad=inventario.stock_actual,
            usuario_id=usuario_id
        )
        db.session.add(nuevo_movimiento)
        
        # Establecer el stock del inventario a 0
        inventario.stock_actual = 0
        db.session.commit()
        
        return jsonify({"mensaje": "Stock del inventario actualizado a 0 y movimiento registrado"}), 200
    
    return jsonify({"error": "Inventario no encontrado"}), 404
