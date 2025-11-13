INSERT INTO customers (name, email, city, signup_date) VALUES
('Paty Martinez', 'paty@gmail.com', 'Monterrey', '2023-10-01'),
('Daniel Sanchez', 'daniel@gmail.com', 'Guadalajara', '2023-10-02'),
('Rafael Sanchez', 'rafael@gmail.com', 'SLP', '2023-10-03'),
('Yael Quintanilla', 'yael@gmail.com', 'CDMX', '2023-10-04');

INSERT INTO products (name, price) VALUES
('MacBook', 40000.00),
('Iphone 17 Pro Max', 50000.00),
('Samsung Galaxy Tab A9', 1999.00),
('Laptop DELL Inspiron 15', 8900.99);

INSERT INTO orders (customer_id, order_date) VALUES
(1, '2023-11-01'),
(2, '2023-11-03'),
(3, '2023-11-05'),
(1, '2023-11-07');

INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 2, 2),
(2, 3, 1),
(3, 4, 1),
(4, 2, 1),
(4, 4, 1);
