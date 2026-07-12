from fastapi import APIRouter

from app.schemas.chat import ChatRequest
from app.schemas.chat import ChatResponse
from app.services.ai_service import AIService

router = APIRouter(tags=["Chat"])

service = AIService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    response = await service.chat(request.message)

    return ChatResponse(
        response=response
    )