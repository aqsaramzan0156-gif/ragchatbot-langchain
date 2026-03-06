# CLAUDE.md - Project Guidelines

## Project Overview

This is a RAG Chatbot application built with LangChain and Ollama. It provides both a FastAPI backend and a Streamlit web interface for AI-powered conversations.

## Project Structure

```
ragchatbot-langchain/
├── src/
│   ├── main.py              # FastAPI app with streaming chat endpoints
│   ├── api/                 # API route handlers
│   ├── config/              # Configuration modules
│   ├── core/                # Core utilities (logging, etc.)
│   ├── providers/           # LLM provider integrations
│   └── services/           # Business logic services
├── app.py                   # Core chatbot engine (main logic)
├── streamlit_app.py         # Professional Streamlit web UI
├── main.py                  # Alternative entry point
├── pyproject.toml           # Project dependencies
└── CLAUDE.md               # This file
```

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Core chatbot engine with token management, LangChain chain setup |
| `src/main.py` | FastAPI application with streaming `/chat` endpoint |
| `streamlit_app.py` | Streamlit web UI with custom dark theme CSS |
| `pyproject.toml` | Project dependencies and metadata |

## Technology Stack

- **Python** 3.11+
- **LangChain** + **langchain-ollama** - LLM framework
- **Ollama** - Local LLM runtime (model: `minimax-m2.5:cloud`)
- **FastAPI** - REST API backend
- **Streamlit** - Web UI framework
- **Tiktoken** - Token counting for context management

## Running the Application

### Streamlit Web UI
```bash
streamlit run streamlit_app.py
```

### FastAPI Server
```bash
uvicorn src.main:app --reload
```

### API Base URL
```
http://localhost:8000
```

## Important Notes

- The chatbot uses token-based context window management (MAX_TOKENS = 2000)
- Model: `minimax-m2.5:cloud` with temperature 0.7
- Streaming is supported via Server-Sent Events (SSE)
- CORS is enabled for all origins in the FastAPI app
- The Streamlit app has custom dark theme CSS styling
- Token trimming logic in `app.py` removes oldest messages when limit is reached

## Code Conventions

- Use Pydantic models for request/response validation
- Follow FastAPI best practices for async endpoints
- LangChain message types: `HumanMessage`, `AIMessage`, `SystemMessage`
- Token counting uses `tiktoken` with `cl100k_base` encoding
- Chat history stored in Streamlit session state as LangChain messages

## Environment Variables

Create `.env` file:
```
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=minimax-m2.5:cloud
TEMPERATURE=0.7
MAX_TOKENS=2000
```

## Key Classes/Functions

| Module | Description |
|--------|-------------|
| `app.py:llm` | ChatOllama instance |
| `app.py:chain` | LangChain prompt + llm + output parser chain |
| `app.py:count_tokens()` | Token counting using tiktoken |
| `app.py:trim_history()` | Removes oldest messages when token limit reached |
| `src/main.py:ChatbotEngine` | FastAPI chatbot engine class |
| `src/main.py:StreamingCallbackHandler` | Callback for streaming responses |
