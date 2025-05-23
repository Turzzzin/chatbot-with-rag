import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from dotenv import load_dotenv

from app.routes.api_router import router as api_v1_router
#from app.api.templates_router import router as templates_router

templates = Jinja2Templates(directory="frontend/templates")


load_dotenv()

app = FastAPI()
app.include_router(api_v1_router, prefix="/api/v1")
#app.include_router(templates_router)