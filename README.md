# RAG Chatbot with LangChain

A production-ready chatbot application built with LangChain and Ollama, featuring both a FastAPI backend and a Streamlit web interface.

## Overview

This project implements an AI-powered chatbot using:bbbb
- **LangChain** - Framework for building LLM applications
- **Ollama** - Local LLM runtime (using `minimax-m2.5:cloud` model)
- **FastAPI** - REST API backend with streaming support
- **Streamlit** - Modern web UI with custom styling

## Features

- **Streaming Responses** - Real-time token-by-token response delivery
- **Context Window Management** - Token-based history trimming (2000 tokens max)
- **Dual Interfaces** - Both API and web UI available
- **CORS Enabled** - Easy integration with frontend applications
- **Professional UI** - Dark-themed Streamlit interface with custom CSS

## Project Structure

```
ragchatbot-langchain/
├── src/
│   ├── main.py          # FastAPI application
│   ├── api/             # API routes
│   ├── config/         # Configuration files
│   ├── core/           # Core utilities
│   ├── models/         # Data models
│   ├── providers/      # LLM providers
│   └── services/       # Business logic
├── app.py              # Core chatbot engine
├── streamlit_app.py    # Streamlit web interface
├── main.py             # Alternative entry point
├── pyproject.toml      # Project dependencies
└── README.md           # This file
```

## Installation

1. **Clone the repository**
   ```bash
   cd ragchatbot-langchain
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirnments.txt
   ```

4. **Configure environment**
   - Copy `.env.example` to `.env`
   - Add your Ollama API settings

5. **Start Ollama**
   ```bash
   ollama serve
   ollama pull minimax-m2.5:cloud
   ```

## Usage

### Option 1: Streamlit Web UI

```bash
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

### Option 2: FastAPI Server

```bash
uvicorn src.main:app --reload
```

Access the API at http://localhost:8000 with interactive docs at http://localhost:8000/docs

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health check |
| `/models` | GET | List available models |
| `/chat` | POST | Send chat message |

### API Usage Example

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "stream": true
  }'
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=minimax-m2.5:cloud
TEMPERATURE=0.7
MAX_TOKENS=2000
```

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MODEL_NAME` | minimax-m2.5:cloud | LLM model to use |
| `TEMPERATURE` | 0.7 | Response creativity (0-1) |
| `MAX_TOKENS` | 2000 | Maximum tokens in context |

## Tech Stack

- **Python** 3.11+
- **LangChain** - LLM framework
- **LangChain Ollama** - Ollama integration
- **FastAPI** - Web framework
- **Streamlit** - UI framework
- **Tiktoken** - Token counting

## Requirements

See `pyproject.toml` for full dependency list:

- langchain-ollama>=1.0.1
- ollama>=0.6.1
- streamlit>=1.55.0
- python-dotenv>=1.2.2
- ipykernel>=7.2.0

## License

MIT License
