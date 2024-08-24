CREATE TABLE productos (
  id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
  nombre VARCHAR(100),
  descripcion TEXT,
  unidad_medida VARCHAR(20),
  status ENUM('agotado', 'faltante', 'entregado', 'sobrante') DEFAULT 'agotado',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  version INT DEFAULT 1
);