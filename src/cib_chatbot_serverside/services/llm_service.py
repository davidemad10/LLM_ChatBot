"""LLM service for chat interactions."""
from typing import List
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage

from ..config.settings import settings
from ..utils.logging import setup_logger

logger = setup_logger("llm_service")


class LLMService:
    """Service for interacting with the LLM."""
    
    def __init__(self):
        logger.info("Initializing LLM...", extra={'stage': 'STARTUP'})
        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=settings.LLM_TEMPERATURE,
        )
        logger.info("LLM initialized successfully")
    
    def invoke(self, messages: List[BaseMessage]) -> AIMessage:
        """Invoke the LLM with a list of messages."""
        logger.info("Invoking LLM...", extra={'stage': 'LLM_INVOCATION'})
        logger.debug(f"Total messages to LLM: {len(messages)}")
        
        response = self.llm.invoke(messages)
        
        logger.info(f"LLM response received", extra={'stage': 'LLM_RESPONSE'})
        logger.debug(f"Response length: {len(response.content)} characters")
        logger.debug(f"Response content:\n{response.content}")
        
        return response
