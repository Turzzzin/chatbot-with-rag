
from fastapi import APIRouter
from app.routes.endpoints.auth import auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/api", tags=["auth"])

