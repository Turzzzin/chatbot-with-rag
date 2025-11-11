import sqlite3
import os
from app.utils.logger import get_logger

logger = get_logger(__name__)

DB_PATH = os.getenv("USER_DB_PATH", "app/data/users.db")

def init_db():
    """Initialize the users database."""
    logger.info("Initializing users database...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Users database initialized.")

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")