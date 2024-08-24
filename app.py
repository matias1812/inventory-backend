from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importa CORS
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Configura CORS para permitir solicitudes desde cualquier origen
CORS(app, resources={r"/api/*": {"origins": "*"}})

from routes.usuario_routes import usuario_bp
from routes.contrato_routes import contrato_bp
from routes.producto_routes import producto_bp
from routes.inventario_routes import inventario_bp
from routes.movimiento_routes import movimiento_bp
from routes.historial_inventario_routes import historial_bp

app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(contrato_bp, url_prefix='/api')
app.register_blueprint(producto_bp, url_prefix='/api')
app.register_blueprint(inventario_bp, url_prefix='/api')
app.register_blueprint(movimiento_bp, url_prefix='/api')
app.register_blueprint(historial_bp, url_prefix='/api')

