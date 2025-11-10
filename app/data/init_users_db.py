import sqlite3
import os

DB_PATH = os.getenv("USER_DB_PATH", "app/data/users.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL
)
""")
conn.commit()
conn.close()
