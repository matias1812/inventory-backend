from flask import Blueprint
from controllers.movimiento_controller import (
    registrar_movimiento, obtener_movimientos, obtener_movimiento,
    actualizar_movimiento, eliminar_movimiento, reporte_movimientos, download_file
)

movimiento_bp = Blueprint('movimiento', __name__)

movimiento_bp.route('/movimientos', methods=['POST'])(registrar_movimiento)
movimiento_bp.route('/movimientos', methods=['GET'])(obtener_movimientos)
movimiento_bp.route('/movimientos/<movimiento_id>', methods=['GET'])(obtener_movimiento)
movimiento_bp.route('/reportes/movimientos', methods=['GET'])(reporte_movimientos)
movimiento_bp.route('/movimientos/<movimiento_id>', methods=['PUT'])(actualizar_movimiento)
movimiento_bp.route('/movimientos/<movimiento_id>', methods=['DELETE'])(eliminar_movimiento)
movimiento_bp.route('/uploads/informes/<filename>', methods=['GET'])(download_file)
