from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.rag_service import initialize_rag
from app.routes.endpoints import chat
from app.routes.endpoints.auth import auth_router

app = FastAPI(title="Medication Chatbot API",
             description="API for medication information using RAG technology",
             version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    app.state.rag_chain = initialize_rag()

app.include_router(chat.router, prefix="/api")
app.include_router(auth_router, prefix="/api")