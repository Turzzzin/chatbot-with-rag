from fastapi import APIRouter, HTTPException, status, Depends
from app.models.schemas import UserCreate, UserLogin, UserOut
from app.services.user_service import create_user, get_user_by_email, verify_password
import os
import jwt

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserOut, tags=["auth"])
def register(user: UserCreate):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    created = create_user(user)
    if not created:
        raise HTTPException(status_code=400, detail="Registration failed")
    return created

@auth_router.post("/login", tags=["auth"])
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": db_user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@auth_router.get("/me", response_model=UserOut, tags=["auth"])
def get_me(token: str = Depends(lambda: None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOut(id=user.id, name=user.name, email=user.email)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
