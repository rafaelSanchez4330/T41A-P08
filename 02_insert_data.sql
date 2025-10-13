
-- Insertar la siguiente cantidad de registros
--4 registros en customers
--4 registros en products
--4 registros en orders
--6 registros en order_items

INSERT INTO customers(name, email, city, signup_date) VALUES 
        ('Cruz Angel Lopez', 'crunchirroll123@gmail.com', 'Salinas', '10-05-2025'),
        ('Yamin Guerrero Guevara', 'yazMAX456@gmail.com', 'Soledad de Graciano Sánchez', '9-25-2025'),
        ('Luis Ángel Vidales Silva', 'angelitobonito@gmail.com', 'Matehuala', '08-15-2025'),
        ('Ximena Patricia Huerta Alvarado', 'minionas123@gmail.com', 'Tepoztlán', '06-30-2025');
        
INSERT INTO products(name, price) VALUES 
        ('Lapiz', 4.5),
        ('Goma', 5),
        ('Sacapuntas', 3.5),
        ('Pluma', 8);

INSERT INTO orders(customer_id, order_date) VALUES 
        (1, now()),
        (3, now()),
        (4, now()),
        (2, now());
        
INSERT INTO order_items(order_id, product_id, quantity) VALUES 
        (1, 2, 1),
        (3, 3, 2),
        (2, 1, 2),
        (4, 4, 3),
        (4, 1, 3),
        (3, 3, 3);
