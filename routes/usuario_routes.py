from flask import Blueprint
from controllers.usuario_controller import registrar_usuario, obtener_usuarios, obtener_usuario, actualizar_usuario, eliminar_usuario, login_usuario, actualizar_rol_usuario

usuario_bp = Blueprint('usuario', __name__)

usuario_bp.route('/signup', methods=['POST'])(registrar_usuario)
usuario_bp.route('/usuarios', methods=['GET'])(obtener_usuarios)
usuario_bp.route('/usuarios/<usuario_id>', methods=['GET'])(obtener_usuario)
usuario_bp.route('/usuarios/<usuario_id>', methods=['PUT'])(actualizar_usuario)
usuario_bp.route('/usuarios/<usuario_id>', methods=['DELETE'])(eliminar_usuario)
usuario_bp.route('/login', methods=['POST'])(login_usuario)
usuario_bp.route('/usuarios/<usuario_id>/rol', methods=['PUT'])(actualizar_rol_usuario)
