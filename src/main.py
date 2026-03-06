# src/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import asyncio
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler
import time

app = FastAPI(title="AI Chat API", description="ChatGPT-like interface")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELS
# ============================================================================
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = "minimax-m2.5:cloud"
    temperature: float = 0.7
    stream: bool = True

class ChatResponse(BaseModel):
    message: Message
    usage: dict

# ============================================================================
# STREAMING CALLBACK
# ============================================================================
class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        super().__init__()
        self.tokens = []
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.tokens.append(token)

# ============================================================================
# CHATBOT ENGINE
# ============================================================================
class ChatbotEngine:
    def __init__(self):
        self.llm = ChatOllama(
            model="minimax-m2.5:cloud",
            temperature=0.7,
            streaming=True
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Provide clear and concise responses."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def convert_messages(self, messages):
        """Convert API messages to LangChain messages"""
        langchain_messages = []
        for msg in messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
        return langchain_messages

# Initialize engine
engine = ChatbotEngine()

# ============================================================================
# API ENDPOINTS
# ============================================================================
@app.get("/")
async def root():
    return {
        "message": "AI Chat API is running",
        "docs": "/docs",
        "chat_endpoint": "/chat"
    }

@app.get("/models")
async def get_models():
    """Get available models"""
    return {"models": ["minimax-m2.5:cloud"]}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with streaming support"""
    
    # Convert messages to LangChain format
    chat_history = engine.convert_messages(request.messages[:-1])  # All except last
    current_message = request.messages[-1].content  # Last message
    
    if request.stream:
        return StreamingResponse(
            stream_response(current_message, chat_history, request.model, request.temperature),
            media_type="text/event-stream"
        )
    else:
        # Non-streaming response
        response = engine.chain.invoke({
            "question": current_message,
            "chat_history": chat_history
        })
        
        return ChatResponse(
            message=Message(role="assistant", content=response),
            usage={"total_tokens": len(response.split())}
        )

async def stream_response(question, chat_history, model, temperature):
    """Stream response from LLM"""
    try:
        # Update model if different
        if model != "minimax-m2.5:cloud":
            engine.llm.model = model
        
        # Stream the response
        async for chunk in engine.chain.astream({
            "question": question,
            "chat_history": chat_history
        }):
            if chunk:
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            await asyncio.sleep(0.01)
        
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

# Run with: uvicorn src.main:app --reload