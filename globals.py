SQLITE3_DB	= "shop.db"
DB_SCHEMA	= ""
"""
"Table: customers (id, name, email, city, created_at)\n" + \
                  "Table: products (id, name, price, in_stock, created_at)\n" + \
                  "Table: orders (id, customer_id, product_id, quantity, order_date, " + \
                    "FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (product_id) REFERENCES products(id))"
"""