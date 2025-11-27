from fastapi import APIRouter, HTTPException, status, Depends
from app.models.schemas import UserCreate, UserLogin, UserOut, Token
from app.services.user_service import create_user, get_user_by_email, verify_password
from app.utils.auth import create_access_token, get_current_user

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="E-mail registrado.")
    created = create_user(user)
    if not created:
        raise HTTPException(status_code=400, detail="Falha no cadastro.")
    return created

@auth_router.post("/login", response_model=Token)
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=UserOut)
def get_me(current_user = Depends(get_current_user)):
    return UserOut(id=current_user.id, name=current_user.name, email=current_user.email)