from flask import Blueprint
from controllers.contrato_controller import registrar_contrato, obtener_contratos, obtener_contrato, actualizar_contrato, eliminar_contrato, get_file

contrato_bp = Blueprint('contrato', __name__)

contrato_bp.route('/contratos', methods=['POST'])(registrar_contrato)
contrato_bp.route('/contratos', methods=['GET'])(obtener_contratos)
contrato_bp.route('/contratos/<contrato_id>', methods=['GET'])(obtener_contrato)
contrato_bp.route('/contratos/<contrato_id>', methods=['PUT'])(actualizar_contrato)
contrato_bp.route('/contratos/<contrato_id>', methods=['DELETE'])(eliminar_contrato)
contrato_bp.route('/contratos/uploads/<path:filename>', methods=['GET'])(get_file)
