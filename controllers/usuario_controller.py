from flask import request, jsonify, current_app
from models.usuario import Usuario
from app import db
from datetime import datetime, timedelta
import jwt
from werkzeug.security import check_password_hash

def login_usuario():
    data = request.json
    print("Datos recibidos:", data)  # Verifica los datos recibidos

    usuario = Usuario.query.filter_by(email=data['email']).first()
    print("Usuario encontrado:", usuario)  # Verifica si el usuario se encontró

    if usuario:
        print("Contraseña almacenada:", usuario.contrasena) 
        print("rol almacenada:", usuario.rol)  # Verifica la contraseña almacenada
        if check_password_hash(usuario.contrasena, data['contrasena']):
            token = jwt.encode({
                'sub': usuario.id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
            return jsonify({"token": token, "rol": usuario.rol, "id": usuario.id}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401

def registrar_usuario():
    data = request.json
    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        rol=data['rol']
    )
    nuevo_usuario.set_password(data['contrasena'])  # Hashea la contraseña
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

def obtener_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.as_dict() for usuario in usuarios]), 200

def obtener_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        return jsonify(usuario.as_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

def actualizar_usuario(usuario_id):
    data = request.json
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        usuario.nombre = data['nombre']
        usuario.email = data['email']
        usuario.set_password(data['contrasena'])  # Hashea la nueva contraseña
        usuario.rol = data['rol']
        db.session.commit()
        return jsonify({"mensaje": "Usuario actualizado exitosamente"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

def actualizar_rol_usuario(usuario_id):
    data = request.json
    usuario = Usuario.query.get(usuario_id)
    
    if usuario:
        usuario.rol = data.get('rol', usuario.rol)  # Actualiza solo el rol
        db.session.commit()
        return jsonify({"mensaje": "Rol del usuario actualizado exitosamente"}), 200
    
    return jsonify({"error": "Usuario no encontrado"}), 404