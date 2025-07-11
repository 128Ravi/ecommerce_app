import sqlite3

con = sqlite3.connect('../db.sqlite3')
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER
)
''')

cur.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user1', 'pass123')")
products = [
    ('Mobile', 15000),
    ('TV', 30000),
    ('Laptop', 50000),
    ('Washing Machine', 20000),
    ('AC', 35000)
]

cur.executemany("INSERT OR IGNORE INTO products (name, price) VALUES (?, ?)", products)

con.commit()
con.close()
print("Database initialized.")
