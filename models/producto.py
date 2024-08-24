from app import db
from uuid import uuid4

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    unidad_medida = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    ubicacion = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    inventarios = db.relationship('Inventario', back_populates='producto')

    def as_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "unidad_medida": self.unidad_medida,
            "status": self.status,
            "ubicacion": self.ubicacion,
            "created_at": self.created_at
        }
