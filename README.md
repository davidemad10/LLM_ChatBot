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
