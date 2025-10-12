from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.utils.logger import logger
import os
router = APIRouter()

@router.get("/", response_class=FileResponse)
async def serve_index():
    logger.info("Serving index.html")
    return FileResponse(os.path.join("frontend", "index.html"))