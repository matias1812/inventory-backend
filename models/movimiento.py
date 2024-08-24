from app import db
from uuid import uuid4

class Movimiento(db.Model):
    __tablename__ = 'movimientos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    inventario_id = db.Column(db.String(36), db.ForeignKey('inventario.id'))
    tipo = db.Column(db.Enum('entrada', 'salida'))
    cantidad = db.Column(db.Integer)
    fecha = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    inventario = db.relationship('Inventario', back_populates='movimientos')
    usuario = db.relationship('Usuario', back_populates='movimientos')

    def as_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': self.tipo,
            'cantidad': self.cantidad,
            'usuario': self.usuario.nombre if self.usuario else 'Desconocido',
            'producto': self.inventario.producto.nombre if self.inventario and self.inventario.producto else 'Desconocido'
        }
