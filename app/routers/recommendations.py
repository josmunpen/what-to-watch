from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import LLMService, get_llm_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, llm: LLMService = Depends(get_llm_service)):
    history = [msg.model_dump() for msg in request.history]
    response_text = llm.run_agent(request.message, history=history)
    return ChatResponse(response=response_text)
