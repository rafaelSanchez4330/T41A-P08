SELECT 
    c.id AS cliente_id,
    c.name AS nombre_cliente,
    o.id AS orden_id,
    o.order_date AS fecha_orden
FROM customers c
JOIN orders o ON c.id = o.customer_id
ORDER BY c.id, o.order_date;

SELECT 
    o.id AS orden_id,
    p.name AS producto,
    oi.quantity AS cantidad,
    p.price AS precio_unitario,
    (oi.quantity * p.price) AS subtotal
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
ORDER BY o.id;

SELECT 
    c.id AS cliente_id,
    c.name AS nombre_cliente,
    SUM(oi.quantity * p.price) AS total_gastado
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY c.id, c.name
ORDER BY total_gastado DESC;

