CREATE TABLE inventario (
  id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
  producto_id VARCHAR(36),
  contrato_id VARCHAR(36),
  stock_inicial INT,
  stock_actual INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES productos(id),
  FOREIGN KEY (contrato_id) REFERENCES contratos(id)
);