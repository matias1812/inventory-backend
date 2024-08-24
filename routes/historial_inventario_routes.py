from flask import Blueprint
from controllers.historial_inventario_controller import registrar_historial, obtener_historiales, obtener_historial, actualizar_historial, eliminar_historial

historial_bp = Blueprint('historial', __name__)

historial_bp.route('/historiales', methods=['POST'])(registrar_historial)
historial_bp.route('/historiales', methods=['GET'])(obtener_historiales)
historial_bp.route('/historiales/<historial_id>', methods=['GET'])(obtener_historial)
historial_bp.route('/historiales/<historial_id>', methods=['PUT'])(actualizar_historial)
historial_bp.route('/historiales/<historial_id>', methods=['DELETE'])(eliminar_historial)
