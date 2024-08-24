from app import db

class HistorialInventario(db.Model):
    __tablename__ = 'historial_inventario'

    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid())
    inventario_id = db.Column(db.String(36), db.ForeignKey('inventario.id'))
    cambio_stock = db.Column(db.Integer)
    fecha = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    tipo_cambio = db.Column(db.Enum('entrada', 'salida'))
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
