-- Tabla: customers
CREATE TABLE customers (
    id SERIAL PRIMARY KEY NOT NULL,                    -- Identificador único autoincremental
    name VARCHAR(40) NOT NULL,                -- Nombre del cliente (obligatorio)
    email VARCHAR(60) NOT NULL UNIQUE,                 -- Email único y obligatorio
    city  VARCHAR(50) NOT NULL,                -- Ciudad del cliente (obligatorio)
    signup_date DATE NOT NULL          -- Fecha de registro (obligatoria)
);
-- Índices para optimizar búsquedas
CREATE INDEX idx_city ON customers(city);              -- Índice para búsquedas por ciudad
CREATE INDEX idx_signup_date ON customers(signup_date);            -- Índice para rangos de fechas

-- Tabla: products
CREATE TABLE products (
    id SERIAL PRIMARY KEY NOT NULL,    -- Identificador único autoincremental
    name VARCHAR(40) NOT NULL,          -- Nombre del producto (obligatorio)
    price REAL NOT NULL                 -- Precio del producto (obligatorio, admite decimales)
);
CREATE INDEX idx_product_name ON products(name);              -- Índice para búsquedas por nombre

-- Tabla: orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY NOT NULL,                  -- Identificador único autoincremental
    customer_id INTEGER NOT NULL,          -- Relación con cliente (clave foránea)
    order_date DATE NOT NULL,          -- Fecha de la orden (obligatoria)
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
CREATE INDEX idx_order_date ON orders(order_date);            -- Índice para rangos de fechas
CREATE INDEX idx_customer_id ON orders(customer_id);             -- Índice para búsquedas por cliente

-- Tabla: order_items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY NOT NULL,            -- Identificador único autoincremental
    order_id INTEGER NOT NULL,             -- Relación con orden (clave foránea)
    product_id INTEGER NOT NULL,          -- Relación con producto (clave foránea)
    quantity INTEGER NOT NULL,              -- Cantidad del producto (obligatoria)
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
CREATE INDEX idx_order_id ON order_items(order_id);            -- Índice para búsquedas por orden
CREATE INDEX idx_product_id ON order_items(product_id);            -- Índice para búsquedas por producto


