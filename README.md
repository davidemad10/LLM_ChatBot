# CIB ChatBot Server Side

A RAG (Retrieval-Augmented Generation) chatbot API built with FastAPI, LangChain, PostgreSQL with pgvector, and Ollama.

## 📋 Features

- **RAG-based Question Answering**: Uses vector similarity search to find relevant context
- **Document Processing**: Automatically processes PDF and Markdown files
- **Chat History**: Maintains conversation context
- **Configurable Prompts**: Easy prompt management through JSON configuration
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **CORS Support**: Ready for frontend integration
- **Environment-based Configuration**: Secure configuration management

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or 3.12
- Poetry (for dependency management)
- PostgreSQL with pgvector extension
- Ollama (running locally with required models)

### Installation

1. **Clone the repository**
   ```bash
   cd CIB_ChatBot_ServerSide
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up PostgreSQL database**
   - Ensure PostgreSQL is running with pgvector extension
   - Create the database and user as specified in `.env`

### Running the Application

#### Start the API Server

```bash
# Using Poetry
poetry run uvicorn cib_chatbot_serverside.main:app --reload

# Or activate the virtual environment first
poetry shell
uvicorn cib_chatbot_serverside.main:app --reload
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative Documentation: `http://localhost:8000/redoc`

#### Sync Documents

To process and index documents from the `data/books` directory:

```bash
# Using Poetry
poetry run python -m cib_chatbot_serverside.scripts.sync_documents

# Or with virtual environment activated
python -m cib_chatbot_serverside.scripts.sync_documents
```

This will:
- Process all existing PDF and Markdown files in the data directory
- Watch for new files and automatically process them

## 📁 Project Structure

```
CIB_ChatBot_ServerSide/
├── src/
│   └── cib_chatbot_serverside/
│       ├── api/                    # API routes and models
│       │   ├── __init__.py
│       │   ├── models.py          # Pydantic models
│       │   └── routes.py          # FastAPI routes
│       ├── config/                 # Configuration management
│       │   ├── __init__.py
│       │   ├── settings.py        # Environment settings
│       │   └── prompts.py         # Prompt configuration
│       ├── db/                     # Database operations
│       │   ├── __init__.py
│       │   ├── connection.py      # DB connection
│       │   └── operations.py      # Vector search & operations
│       ├── services/               # Business logic
│       │   ├── __init__.py
│       │   ├── llm_service.py     # LLM interactions
│       │   └── rag_service.py     # RAG logic
│       ├── scripts/                # Utility scripts
│       │   ├── __init__.py
│       │   └── sync_documents.py  # Document processing
│       ├── utils/                  # Utilities
│       │   ├── __init__.py
│       │   └── logging.py         # Logging configuration
│       ├── __init__.py
│       ├── main.py                 # FastAPI app entry point
│       └── prompt_config.json      # Prompt templates
├── tests/                          # Test files
├── data/                           # Data directory (gitignored)
│   └── books/                      # Place your documents here
├── logs/                           # Log files (gitignored)
├── .env                            # Environment variables (gitignored)
├── .env.example                    # Example environment config
├── pyproject.toml                  # Project dependencies
└── README.md                       # This file
```

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options. Key settings:

- **Database**: PostgreSQL connection details
- **Ollama**: Base URL and model names
- **RAG**: Similarity threshold and top-k results
- **Logging**: Log directory and level

### Prompt Configuration

Edit `src/cib_chatbot_serverside/prompt_config.json` to customize:
- System message
- Prompt template
- Default similarity threshold
- Default top-k results

## 📡 API Endpoints

### `POST /api/chat`
Send a chat message and receive a response.

**Request:**
```json
{
  "message": "What is machine learning?"
}
```

**Response:**
```json
{
  "response": "Machine learning is...",
  "context_used": true,
  "sources": ["file1.pdf", "file2.md"]
}
```

### `POST /api/clear-history`
Clear the chat conversation history.

### `GET /api/health`
Health check endpoint.

### `GET /`
Root endpoint with API information.

## 🧪 Testing

```bash
poetry run pytest
```

## 📝 Development

### Adding New Features

1. **API Endpoints**: Add routes in `src/cib_chatbot_serverside/api/routes.py`
2. **Business Logic**: Implement services in `src/cib_chatbot_serverside/services/`
3. **Database Operations**: Add functions in `src/cib_chatbot_serverside/db/operations.py`

### Code Organization Principles

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Services are injected where needed
- **Configuration**: All config in environment variables and JSON files
- **Logging**: Comprehensive logging throughout the application

## 🐛 Troubleshooting

### Import Errors
Make sure to run the application from the correct module path:
```bash
uvicorn cib_chatbot_serverside.main:app --reload
```

### Database Connection Issues
- Verify PostgreSQL is running
- Check `.env` database credentials
- Ensure pgvector extension is installed

### Ollama Model Issues
- Ensure Ollama is running: `ollama serve`
- Pull required models:
  ```bash
  ollama pull llama3.1:8b
  ollama pull mxbai-embed-large
  ```

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Name]

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
