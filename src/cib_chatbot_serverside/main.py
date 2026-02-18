"""Main FastAPI application."""
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .config.settings import settings
from .utils.logging import setup_logger

logger = setup_logger("main")

# Create FastAPI app
app = FastAPI(
    title="CIB ChatBot API",
    description="RAG-based chatbot API using LangChain and PostgreSQL with pgvector",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests."""
    request_id = f"{time.time()}"
    logger.info(f"Request started", extra={'stage': 'HTTP_REQUEST'})
    logger.debug(f"Request ID: {request_id}")
    logger.debug(f"Method: {request.method}")
    logger.debug(f"URL: {request.url}")
    logger.debug(f"Client: {request.client.host if request.client else 'Unknown'}")
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"Request completed in {process_time:.4f} seconds", extra={'stage': 'HTTP_RESPONSE'})
    logger.debug(f"Response status: {response.status_code}")
    
    return response


# Include API routes
app.include_router(router, prefix="/api", tags=["chat"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "CIB ChatBot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "clear_history": "/api/clear-history",
            "health": "/api/health",
            "docs": "/docs"
        }
    }


def main():
    """Entry point for the application."""
    import uvicorn
    uvicorn.run(
        "cib_chatbot_serverside.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )


if __name__ == "__main__":
    main()
