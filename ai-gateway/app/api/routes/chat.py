from fastapi import APIRouter

from app.schemas.chat import ChatRequest
from app.services.ai_service import AIService

router = APIRouter(tags=["Chat"])

service = AIService()


@router.post("/chat")
async def chat(request: ChatRequest):
    return await service.chat(request.message)