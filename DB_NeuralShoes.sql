-- ============================================================================================== -- Base de datos: NeuralShoes 
-- ==============================================================================================
-- ----------------------------------------------------------------------------------------------
-- 1. Tabla Clientes
CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ----------------------------------------------------------------------------------------------    
-- 2. Tabla Categorías
CREATE TABLE categoria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);
-- ----------------------------------------------------------------------------------------------
-- 3. Tabla Marcas
CREATE TABLE marca (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- ----------------------------------------------------------------------------------------------
CREATE TABLE marca_categorias (
    marca_id INT REFERENCES marca(id) ON DELETE CASCADE,
    categoria_id INT REFERENCES categoria(id) ON DELETE CASCADE,
    PRIMARY KEY (marca_id, categoria_id)
);
-- ----------------------------------------------------------------------------------------------
-- 5. Tabla Productos
CREATE TABLE producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    marca_id INT REFERENCES marca(id) ON DELETE CASCADE
);
-- ----------------------------------------------------------------------------------------------
-- 6. Tabla Tallas
CREATE TABLE talla (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(10) UNIQUE NOT NULL
);
-- ----------------------------------------------------------------------------------------------
-- 7. Tabla TallaProducto (producto con múltiples tallas y stock por talla)
CREATE TABLE talla_producto (
    id SERIAL PRIMARY KEY,
    producto_id INT REFERENCES producto(id) ON DELETE CASCADE,
    stock INTEGER DEFAULT 0
);
-- ----------------------------------------------------------------------------------------------
-- 8. Relación N:M entre talla_producto y talla
CREATE TABLE talla_producto_tallas (
    talla_producto_id INT REFERENCES talla_producto(id) ON DELETE CASCADE,
    talla_id INT REFERENCES talla(id) ON DELETE CASCADE,
    PRIMARY KEY (talla_producto_id, talla_id)
);
-- ----------------------------------------------------------------------------------------------
-- 9. Tabla Pedidos
CREATE TABLE pedido (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente(id) ON DELETE CASCADE,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) CHECK (estado IN ('Pendiente', 'Enviado', 'Entregado', 'Cancelado'))
);
-- ----------------------------------------------------------------------------------------------
-- 10. Tabla DetallePedido (controla pedidos por talla específica)
CREATE TABLE detalle_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedido(id) ON DELETE CASCADE,
    talla_producto_id INT REFERENCES talla_producto(id) ON DELETE CASCADE,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    UNIQUE (pedido_id, talla_producto_id)
);
--  ----------------------------------------------------------------------------------------------
-- 11. Tabla Pagos
CREATE TABLE pago (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedido(id) ON DELETE CASCADE,
    metodo_pago VARCHAR(50) CHECK (metodo_pago IN ('Tarjeta', 'Efectivo', 'Transferencia', 'PayPal')),
    monto DECIMAL(10,2) NOT NULL,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);