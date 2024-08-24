from flask import Blueprint
from controllers.producto_controller import registrar_producto, obtener_productos, obtener_producto, actualizar_producto, eliminar_producto

producto_bp = Blueprint('productos', __name__)

producto_bp.route('/productos', methods=['POST'])(registrar_producto)
producto_bp.route('/productos', methods=['GET'])(obtener_productos)
producto_bp.route('/productos/<producto_id>', methods=['GET'])(obtener_producto)
producto_bp.route('/productos/<producto_id>', methods=['PUT'])(actualizar_producto)
producto_bp.route('/productos/<producto_id>', methods=['DELETE'])(eliminar_producto)
