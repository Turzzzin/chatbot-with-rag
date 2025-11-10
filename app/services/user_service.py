from passlib.context import CryptContext
from typing import Optional
from pydantic import EmailStr
from app.models.schemas import UserCreate, UserLogin, User, UserOut
import sqlite3
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DB_PATH = os.getenv("USER_DB_PATH", "app/data/users.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(user: UserCreate) -> Optional[UserOut]:
    hashed_password = pwd_context.hash(user.password)
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (name, email, hashed_password)
            VALUES (?, ?, ?)
        """, (user.name, user.email, hashed_password))
        conn.commit()
        user_id = cur.lastrowid
        return UserOut(id=user_id, name=user.name, email=user.email)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email: EmailStr) -> Optional[User]:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(id=row["id"], name=row["name"], email=row["email"], hashed_password=row["hashed_password"])
    return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
