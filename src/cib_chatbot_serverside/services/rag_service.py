"""RAG (Retrieval-Augmented Generation) service."""
import time
from typing import List, Tuple, Dict, Any
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ..db.operations import similarity_search_with_scores
from ..config.prompts import prompt_manager
from ..config.settings import settings
from ..utils.logging import setup_logger
from .llm_service import LLMService

logger = setup_logger("rag_service")


class RAGService:
    """Service for RAG-based question answering."""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.chat_history: List[HumanMessage | AIMessage] = []
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query using RAG."""
        total_start_time = time.time()
        
        # Load configuration
        config = prompt_manager.get()
        prompt_template = config["prompt_template"]
        similarity_threshold = config.get("similarity_threshold", settings.SIMILARITY_THRESHOLD)
        top_k = config.get("top_k_results", settings.TOP_K_RESULTS)
        system = SystemMessage(content=config["system_message"])
        
        logger.info("=" * 80, extra={'stage': 'NEW_CHAT_REQUEST'})
        logger.info(f"New chat request received")
        logger.info(f"User query: {query}", extra={'stage': 'USER_INPUT'})
        logger.debug(f"Query length: {len(query)} characters")
        logger.debug(f"Current chat history length: {len(self.chat_history)} messages")
        
        # Perform similarity search
        search_start_time = time.time()
        results = similarity_search_with_scores(query, k=top_k)
        search_time = time.time() - search_start_time
        logger.info(f"Total search time: {search_time:.4f} seconds")
        
        # Determine response strategy
        logger.info("Evaluating response strategy...", extra={'stage': 'RESPONSE_STRATEGY'})
        
        if len(results) == 0 or results[0][1] < similarity_threshold:
            logger.info("Strategy: Using general knowledge (low relevance or no results)")
            logger.debug(
                f"Reason: {'No results found' if len(results) == 0 else f'Best similarity score ({results[0][1]:.4f}) below threshold ({similarity_threshold})'}"
            )
            
            messages = [system] + self.chat_history + [HumanMessage(content=query)]
            context_used = False
        else:
            logger.info("Strategy: Using RAG context")
            logger.debug(f"Best similarity score: {results[0][1]:.4f}")
            
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            logger.info(f"Context prepared", extra={'stage': 'CONTEXT_PREPARATION'})
            logger.debug(f"Total context length: {len(context_text)} characters")
            logger.debug(f"Context sources: {[doc.metadata.get('file_name', 'unknown') for doc, _ in results]}")
            
            prompt = prompt_template.format(context=context_text, question=query)
            logger.debug(f"Final prompt length: {len(prompt)} characters")
            
            messages = [system] + self.chat_history + [HumanMessage(content=prompt)]
            context_used = True
        
        # Invoke LLM
        llm_start_time = time.time()
        response = self.llm_service.invoke(messages)
        llm_time = time.time() - llm_start_time
        
        response_text = response.content
        
        # Update chat history
        self.chat_history.append(HumanMessage(content=query))
        self.chat_history.append(AIMessage(content=response_text))
        logger.debug(f"Chat history updated. New length: {len(self.chat_history)} messages")
        
        # Final summary
        total_time = time.time() - total_start_time
        logger.info("=" * 80, extra={'stage': 'REQUEST_SUMMARY'})
        logger.info(f"Request completed successfully")
        logger.info(f"Total processing time: {total_time:.4f} seconds")
        logger.info(f"  - Search time: {search_time:.4f} seconds")
        logger.info(f"  - LLM time: {llm_time:.4f} seconds")
        logger.info(f"Context used: {context_used}")
        logger.info(f"Results found: {len(results)}")
        if results:
            logger.info(f"Best similarity: {results[0][1]:.4f}")
            logger.info(f"Source files: {[doc.metadata.get('file_name', 'unknown') for doc, _ in results]}")
        logger.info("=" * 80)
        
        return {
            "response": response_text,
            "context_used": context_used,
            "sources": [doc.metadata.get('file_name', 'unknown') for doc, _ in results] if results else []
        }
    
    def clear_history(self):
        """Clear the chat history."""
        self.chat_history.clear()
        logger.info("Chat history cleared")
