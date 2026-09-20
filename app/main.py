import os
import time
import asyncio
from typing import List, Optional, AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(
    title="AI Chat Assistant & Tool Gateway",
    version="1.1.0",
    description="Multi-model orchestration gateway with tool calling and SSE streaming support."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "gemini-2.0-flash"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    id: str
    model: str
    content: str
    latency_ms: float

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.1.0",
        "providers": {
            "gemini": "configured" if os.getenv("GEMINI_API_KEY") else "mock",
            "anthropic": "configured" if os.getenv("ANTHROPIC_API_KEY") else "mock"
        }
    }

async def fake_token_stream(prompt: str, model: str) -> AsyncGenerator[str, None]:
    """Simulate low-latency token streaming for local and upstream tests."""
    words = f"[{model}] Response to: {prompt}. Streaming tokens via Server-Sent Events with zero buffering.".split(" ")
    for word in words:
        yield f"data: {word} \n\n"
        await asyncio.sleep(0.05)
    yield "data: [DONE]\n\n"

@app.post("/v1/chat")
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    
    if not request.messages:
        raise HTTPException(status_code=400, detail="Message list cannot be empty.")
    
    user_prompt = request.messages[-1].content
    
    if request.stream:
        return StreamingResponse(
            fake_token_stream(user_prompt, request.model),
            media_type="text/event-stream"
        )
    
    reply = f"Processed query using {request.model}: '{user_prompt}'"
    latency = round((time.time() - start_time) * 1000, 2)
    
    return ChatResponse(
        id=f"chat-{int(time.time())}",
        model=request.model,
        content=reply,
        latency_ms=latency
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
