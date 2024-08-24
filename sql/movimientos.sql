CREATE TABLE movimientos (
  id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
  inventario_id VARCHAR(36),
  tipo ENUM('entrada', 'salida'),
  cantidad INT,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  usuario_id VARCHAR(36),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (inventario_id) REFERENCES inventario(id),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);