# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
poetry install
```

### 2. Configure Environment
```bash
# The .env file is already created with defaults
# Edit if you need to change database credentials or other settings
notepad .env
```

### 3. Start the Server

**Option A: Using Poetry (recommended)**
```bash
poetry run uvicorn cib_chatbot_serverside.main:app --reload
```

**Option B: Activate virtual environment first**
```bash
poetry shell
uvicorn cib_chatbot_serverside.main:app --reload
```

**Option C: Using the script entry point**
```bash
poetry run chatbot-server
```

### 4. Test the API

Open your browser and go to:
- **API Documentation**: http://localhost:8000/docs
- **API Root**: http://localhost:8000/

Or test with curl:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### 5. Sync Documents (Optional)

To process PDF and Markdown files from `data/books/`:

```bash
# Place your files in data/books/ directory
mkdir -p data/books

# Run the sync script
poetry run python -m cib_chatbot_serverside.scripts.sync_documents

# Or use the shortcut
poetry run sync-docs
```

## Project Structure Overview

```
CIB_ChatBot_ServerSide/
├── src/cib_chatbot_serverside/
│   ├── main.py              # ⭐ FastAPI app entry point
│   ├── api/                 # API routes and models
│   ├── services/            # Business logic (RAG, LLM)
│   ├── db/                  # Database operations
│   ├── config/              # Configuration management
│   ├── scripts/             # Utility scripts
│   └── utils/               # Logging and utilities
├── tests/                   # Test files
├── data/books/              # Your documents (PDF, MD)
├── logs/                    # Application logs
├── .env                     # Environment configuration
└── README.md                # Full documentation
```

## Common Commands

```bash
# Start server
poetry run uvicorn cib_chatbot_serverside.main:app --reload

# Sync documents
poetry run python -m cib_chatbot_serverside.scripts.sync_documents

# Run tests
poetry run pytest

# Check for errors
poetry run python -c "from cib_chatbot_serverside import settings; print('OK')"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/api/health` | GET | Health check |
| `/api/chat` | POST | Send a chat message |
| `/api/clear-history` | POST | Clear chat history |
| `/docs` | GET | Interactive API documentation |

## Troubleshooting

### "Module not found" error
```bash
poetry install
```

### Database connection error
- Check PostgreSQL is running
- Verify credentials in `.env`
- Ensure pgvector extension is installed

### Ollama model not found
```bash
ollama pull llama3.1:8b
ollama pull mxbai-embed-large
```

## Next Steps

1. ✅ Server is running
2. 📚 Add documents to `data/books/`
3. 🔄 Run document sync
4. 💬 Start chatting!

For more details, see [README.md](README.md) and [MIGRATION.md](MIGRATION.md).
