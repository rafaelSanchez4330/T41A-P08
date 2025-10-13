--CONSULTAS 
-- Clientes y sus órdenes
SELECT c.id AS id_cliente, c.name AS nombre_cliente, o.id AS id_orden, o.order_date AS fecha_orden
FROM customers c 
JOIN orders o ON o.customer_id = c.id;

-- Órdenes y sus productos
SELECT  o.id AS id_orden, 
        oi.product_id AS id_producto,
        p.name AS nombre_producto,
        p.price AS precio_producto,
        oi.quantity AS cantidad
FROM orders o 
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id;
-- Total gastado por cliente
SELECT  c.id AS id_cliente,
        c.name AS nombre_cliente,
        o.id AS id_orden,
        o.order_date AS fecha_compra,
        SUM(oi.quantity * p.price) AS total_orden
FROM customers c 
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.id, c.name, o.id, o.order_date
ORDER BY o.order_date;

