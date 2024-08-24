from app import db
from uuid import uuid4

class Inventario(db.Model):
    __tablename__ = 'inventario'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    producto_id = db.Column(db.String(36), db.ForeignKey('productos.id'))
    contrato_id = db.Column(db.String(36), db.ForeignKey('contratos.id'))
    stock_inicial = db.Column(db.Integer)
    stock_actual = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())

    producto = db.relationship('Producto', back_populates='inventarios')
    movimientos = db.relationship('Movimiento', back_populates='inventario')

    def as_dict(self):
        return {
            "id": self.id,
            "producto_id": self.producto_id,
            "contrato_id": self.contrato_id,
            "stock_inicial": self.stock_inicial,
            "stock_actual": self.stock_actual,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
