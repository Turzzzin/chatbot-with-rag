from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import get_rag_response
from app.utils.logger import logger
from fastapi import Request
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request_body: ChatRequest, request: Request, user = Depends(get_current_user)):
    try:
        logger.info(f"Received question")
        answer, sources = await get_rag_response(request_body.question, request)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
