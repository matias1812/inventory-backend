from app import db

class Contrato(db.Model):
    __tablename__ = 'contratos'

    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid())
    numero_contrato = db.Column(db.String(50), unique=True)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    archivo_path = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())
    version = db.Column(db.Integer, default=1)

    def as_dict(self):
        return {
            "id": self.id,
            "numero_contrato": self.numero_contrato,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "archivo_path": self.archivo_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version
        }
