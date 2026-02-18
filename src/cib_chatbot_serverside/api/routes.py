"""API routes for the chat application."""
from fastapi import APIRouter, Request
import time

from .models import ChatRequest, ChatResponse
from ..services import RAGService
from ..utils.logging import setup_logger

logger = setup_logger("api_routes")

router = APIRouter()

# Initialize RAG service
rag_service = RAGService()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """Chat endpoint that processes user queries using RAG."""
    result = rag_service.process_query(req.message)
    return ChatResponse(**result)


@router.post("/clear-history")
async def clear_history():
    """Clear the chat history."""
    rag_service.clear_history()
    return {"message": "Chat history cleared"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
