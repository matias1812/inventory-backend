CREATE TABLE historial_inventario (
  id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
  inventario_id VARCHAR(36),
  cambio_stock INT,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  tipo_cambio ENUM('entrada', 'salida'),
  usuario_id VARCHAR(36),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (inventario_id) REFERENCES inventario(id),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);