from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
router = APIRouter()

@router.get("/", response_class=FileResponse)
async def serve_index():
    return FileResponse(os.path.join("frontend", "index.html"))