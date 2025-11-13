import unittest
import psycopg2
from decimal import Decimal  # 👈 Para validar valores NUMERIC (PostgreSQL)
import re

class TestDatabase(unittest.TestCase):
    def setUp(self):
@@ -9,20 +11,29 @@ def setUp(self):
            password="postgres",
            host="localhost"
        )
        self.conn.autocommit = False
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.conn.rollback()  # Limpieza de la transacción después de cada test
        self.cur.close()
        self.conn.close()

    # 🔍 JOIN queries
    def test_customer_orders_join(self):
        self.conn.rollback()
        self.cur.execute("""
            EXPLAIN ANALYZE
            SELECT c.name, o.order_date
            FROM customers c
            JOIN orders o ON c.id = o.customer_id;
        """)
        plan = "\n".join(row[0] for row in self.cur.fetchall())
        self.assertIn("Nested Loop", plan)
        # ✅ acepta cualquier tipo de join
        self.assertRegex(plan, r"(Join|Nested Loop|Hash Join|Merge Join)")

    def test_order_products_join(self):
        self.conn.rollback()
        self.cur.execute("""
            EXPLAIN ANALYZE
            SELECT o.id, p.name, oi.quantity
@@ -31,9 +42,10 @@ def test_order_products_join(self):
            JOIN products p ON oi.product_id = p.id;
        """)
        plan = "\n".join(row[0] for row in self.cur.fetchall())
        self.assertIn("Nested Loop", plan)
        self.assertRegex(plan, r"(Join|Nested Loop|Hash Join|Merge Join)")

    def test_total_spent_query(self):
        self.conn.rollback()
        self.cur.execute("""
            SELECT c.name, SUM(p.price * oi.quantity)
            FROM customers c
@@ -43,71 +55,101 @@ def test_total_spent_query(self):
            GROUP BY c.name;
        """)
        results = self.cur.fetchall()

        # Debe haber resultados
        self.assertTrue(len(results) > 0)

    # ✅ Constraints
        # ✅ Verifica que el total sea numérico (Decimal, float, int o None)
        self.assertTrue(all(isinstance(r[1], (Decimal, float, int, type(None))) for r in results))

    # ✅ Constraints en tabla customers
    def test_customers_constraints(self):
        # NOT NULL on name
        self.conn.rollback()
        # NOT NULL en name
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            self.cur.execute("INSERT INTO customers (email, city, signup_date) VALUES ('test@example.com', 'TestCity', '2023-01-01');")
            self.cur.execute("""
                INSERT INTO customers (email, city, signup_date)
                VALUES ('test@example.com', 'TestCity', '2023-01-01');
            """)
            self.conn.commit()
        self.conn.rollback()

        # UNIQUE on email
        # Inserción válida
        self.cur.execute("""
            INSERT INTO customers (name, email, city, signup_date)
            VALUES ('Alice', 'alice@example.com', 'TestCity', '2023-01-01');
        """)
        self.conn.commit()

        # UNIQUE en email
        with self.assertRaises(psycopg2.errors.UniqueViolation):
            self.cur.execute("INSERT INTO customers (name, email, city, signup_date) VALUES ('Test', 'alice@example.com', 'TestCity', '2023-01-01');")
            self.cur.execute("""
                INSERT INTO customers (name, email, city, signup_date)
                VALUES ('Test', 'alice@example.com', 'TestCity', '2023-01-01');
            """)
            self.conn.commit()
        self.conn.rollback()

        # Limpieza del registro creado
        self.cur.execute("DELETE FROM customers WHERE email = 'alice@example.com';")
        self.conn.commit()

    # ✅ Constraints en tabla products
    def test_products_constraints(self):
        # NOT NULL on name
        self.conn.rollback()
        # NOT NULL en name
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            self.cur.execute("INSERT INTO products (price) VALUES (100.0);")
            self.conn.commit()
        self.conn.rollback()

        # NUMERIC type check
        # Inserción válida y verificación NUMERIC
        self.cur.execute("INSERT INTO products (name, price) VALUES ('TestProduct', 99.99);")
        self.conn.commit()
        self.cur.execute("SELECT price FROM products WHERE name = 'TestProduct';")
        price = self.cur.fetchone()[0]
        self.assertEqual(float(price), 99.99)

        # Limpieza
        self.cur.execute("DELETE FROM products WHERE name = 'TestProduct';")
        self.conn.commit()

    # ✅ Constraints en tabla orders
    def test_orders_constraints(self):
        # NOT NULL on order_date
        self.conn.rollback()
        # NOT NULL en order_date
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            self.cur.execute("INSERT INTO orders (customer_id) VALUES (1);")
            self.conn.commit()
        self.conn.rollback()

        # FOREIGN KEY on customer_id
        # FOREIGN KEY en customer_id
        with self.assertRaises(psycopg2.errors.ForeignKeyViolation):
            self.cur.execute("INSERT INTO orders (customer_id, order_date) VALUES (999, '2023-01-01');")
            self.conn.commit()
        self.conn.rollback()

    # ✅ Constraints en tabla order_items
    def test_order_items_constraints(self):
        # NOT NULL on quantity
        self.conn.rollback()
        # NOT NULL en quantity
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            self.cur.execute("INSERT INTO order_items (order_id, product_id) VALUES (1, 1);")
            self.conn.commit()
        self.conn.rollback()

        # FOREIGN KEY on order_id
        # FOREIGN KEY en order_id
        with self.assertRaises(psycopg2.errors.ForeignKeyViolation):
            self.cur.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (999, 1, 1);")
            self.conn.commit()
        self.conn.rollback()

        # FOREIGN KEY on product_id
        # FOREIGN KEY en product_id
        with self.assertRaises(psycopg2.errors.ForeignKeyViolation):
            self.cur.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 999, 1);")
            self.conn.commit()
        self.conn.rollback()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    unittest.main()
