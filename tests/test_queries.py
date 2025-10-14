import unittest
import psycopg2
import re

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="test_db",
            user="postgres",
            password="postgres",
            host="localhost"
        )
        self.cur = self.conn.cursor()
        self.cur.execute("BEGIN;")

    # 🔍 JOIN queries
    def test_customer_orders_join(self):
       
        self.cur.execute("""
            EXPLAIN ANALYZE
            SELECT c.name, o.order_date
            FROM customers c
            JOIN orders o ON c.id = o.customer_id;
        """)
        plan = "\n".join(row[0] for row in self.cur.fetchall())
        self.assertRegex(plan, r"(Nested Loop|Hash Join|Merge Join)")

    def test_order_products_join(self):
        self.cur.execute("""
            EXPLAIN ANALYZE
            SELECT o.id, p.name, oi.quantity
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id;
        """)
        plan = "\n".join(row[0] for row in self.cur.fetchall())
        self.assertRegex(plan, r"(Nested Loop|Hash Join|Merge Join)")

    def test_total_spent_query(self):
         self.cur.execute("SET enable_hashjoin = OFF;")
        self.cur.execute("SET enable_mergejoin = OFF;")
        self.cur.execute("""
            SELECT c.name, SUM(p.price * oi.quantity)
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            GROUP BY c.name;
        """)
        results = self.cur.fetchall()
        self.assertTrue(len(results) > 0)

    # ✅ Constraints
    def test_customers_constraints(self):
        # NOT NULL on name
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            self.cur.execute("INSERT INTO customers (email, city, signup_date) VALUES ('test@example.com', 'TestCity', '2023-01-01');")
            self.conn.commit()
        self.conn.rollback()

        # UNIQUE on email
        with self.assertRaises(psycopg2.errors.UniqueViolation):
            self.cur.execute("INSERT INTO customers (name, email, city, signup_date) VALUES ('Test', 'yazMAX456@gmail.com', 'TestCity', '2023-01-01');")
            self.conn.commit()
        self.conn.rollback()

    def test_products_constraints(self):
        # NOT NULL on name
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            self.cur.execute("INSERT INTO products (price) VALUES (100.0);")
            self.conn.commit()
        self.conn.rollback()

        # NUMERIC type check
        self.cur.execute("INSERT INTO products (name, price) VALUES ('TestProduct', 99.99);")
        self.conn.commit()
        self.cur.execute("SELECT price FROM products WHERE name = 'TestProduct';")
        price = self.cur.fetchone()[0]
        self.assertEqual(float(price), 99.99)

    def test_orders_constraints(self):
        # NOT NULL on order_date
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            self.cur.execute("INSERT INTO orders (customer_id) VALUES (1);")
            self.conn.commit()
        self.conn.rollback()

        # FOREIGN KEY on customer_id
        with self.assertRaises(psycopg2.errors.ForeignKeyViolation):
            self.cur.execute("INSERT INTO orders (customer_id, order_date) VALUES (999, '2023-01-01');")
            self.conn.commit()
        self.conn.rollback()

    def test_order_items_constraints(self):
        # NOT NULL on quantity
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            self.cur.execute("INSERT INTO order_items (order_id, product_id) VALUES (1, 1);")
            self.conn.commit()
        self.conn.rollback()

        # FOREIGN KEY on order_id
        with self.assertRaises(psycopg2.errors.ForeignKeyViolation):
            self.cur.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (999, 1, 1);")
            self.conn.commit()
        self.conn.rollback()

        # FOREIGN KEY on product_id
        with self.assertRaises(psycopg2.errors.ForeignKeyViolation):
            self.cur.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 999, 1);")
            self.conn.commit()
        self.conn.rollback()

    def tearDown(self):
        self.conn.rollback()
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    unittest.main()
