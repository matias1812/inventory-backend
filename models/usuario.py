from app import db
from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo para la tabla 'Usuarios'
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('admin', 'usuario'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    movimientos = db.relationship('Movimiento', backref='usuarios')

    def set_password(self, password):
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena, password)

    def as_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }