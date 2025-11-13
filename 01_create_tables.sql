CREATE TABLE customers (
    id SERIAL PRIMARY KEY NOT NULL,                          
    name TEXT NOT NULL,                             
    email TEXT UNIQUE NOT NULL,   
    city TEXT NOT NULL,                           
    signup_date DATE NOT NULL                       
);

CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_customers_signup_date ON customers(signup_date);

CREATE TABLE products (
    id SERIAL PRIMARY KEY NOT NULL,                    
    name TEXT NOT NULL,                          
    price NUMERIC(10,2) NOT NULL
);

CREATE INDEX idx_products_name ON products(name); 

CREATE TABLE orders (
    id SERIAL PRIMARY KEY NOT NULL,  
    customer_id INTEGER REFERENCES customers(id),
    order_date DATE NOT NULL
);

CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY NOT NULL, 
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
