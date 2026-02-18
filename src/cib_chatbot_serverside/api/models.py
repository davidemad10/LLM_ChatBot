"""API request and response models."""
from typing import List, Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    context_used: Optional[bool] = None
    sources: Optional[List[str]] = None
