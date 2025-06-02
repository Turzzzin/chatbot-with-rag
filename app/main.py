from fastapi import FastAPI
from app.services.rag_service import initialize_rag
from app.routes.endpoints import chat
from app.routes.endpoints import home
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.on_event("startup")
async def startup_event():
    app.state.rag_chain = initialize_rag()  

app.include_router(chat.router)
app.include_router(home.router)
