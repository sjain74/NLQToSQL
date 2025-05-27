import sqlite3
import random
from faker import Faker
import globals

# Initialize Faker and database
faker = Faker()
conn = sqlite3.connect(globals.SQLITE3_DB)
cursor = conn.cursor()

# Insert sample customers
customers = [(faker.name(), faker.unique.email(), faker.city()) for _ in range(1000)]
cursor.executemany("INSERT INTO customers (name, email, city) VALUES (?, ?, ?)", customers)

# Insert sample products
products = [(faker.word().capitalize(), round(random.uniform(10.0, 1000.0), 2)) for _ in range(500)]
cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", products)

# Insert sample orders
orders = [
    (random.randint(1, 1000), random.randint(1, 500), random.randint(1, 5))
    for _ in range(10000)
]
cursor.executemany("INSERT INTO orders (customer_id, product_id, quantity) VALUES (?, ?, ?)", orders)

# Commit and close
conn.commit()
conn.close()

print("Database with 1000 customers, 500 products, and 10000 orders created.")
