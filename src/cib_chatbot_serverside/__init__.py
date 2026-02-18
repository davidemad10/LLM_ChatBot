"""
CIB ChatBot Server Side
A RAG-based chatbot API using FastAPI, LangChain, and PostgreSQL with pgvector
"""

__version__ = "1.0.0"

# Make key components available at package level
from .config import settings, prompt_manager
from .services import RAGService, LLMService
from .api import ChatRequest, ChatResponse

__all__ = [
    "settings",
    "prompt_manager",
    "RAGService",
    "LLMService",
    "ChatRequest",
    "ChatResponse",
]
