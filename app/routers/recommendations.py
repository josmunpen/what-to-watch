from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.services.llm_service import graph

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Invocamos el grafo con el mensaje del usuario como estado inicial.
    # LangGraph ejecuta el nodo "chatbot" y devuelve el estado final.
    result = graph.invoke({"messages": [HumanMessage(content=request.message)]})

    # El último mensaje en el estado es la respuesta del LLM
    response_text = result["messages"][-1].content
    return ChatResponse(response=response_text)