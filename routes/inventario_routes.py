from flask import Blueprint
from controllers.inventario_controller import registrar_inventario, obtener_inventarios, obtener_inventario, actualizar_inventario, eliminar_inventario

inventario_bp = Blueprint('inventario', __name__)

inventario_bp.route('/inventarios', methods=['POST'])(registrar_inventario)
inventario_bp.route('/inventarios', methods=['GET'])(obtener_inventarios)
inventario_bp.route('/inventarios/<inventario_id>', methods=['GET'])(obtener_inventario)
inventario_bp.route('/inventarios/<inventario_id>', methods=['PUT'])(actualizar_inventario)
inventario_bp.route('/inventarios/<inventario_id>/usuario/<usuario_id>', methods=['DELETE'])(eliminar_inventario)
