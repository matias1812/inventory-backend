# controllers/grafico_controller.py
from flask import request, jsonify
from utils.graph import generar_grafico

def generar_grafico_route():
    data = request.json
    graph = generar_grafico(
        data['tipo'],
        data['datos'],
        data['titulo'],
        data['xlabel'],
        data['ylabel']
    )
    return jsonify({"grafico": graph})
