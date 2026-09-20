# AI Chat Assistant & Tool Gateway

A lightweight, high-throughput AI chat gateway built with Python and FastAPI. It orchestrates requests across Anthropic Claude, Google Gemini, and local models with built-in streaming, fallback routing, and tool-calling execution.

## Features

- **Multi-Model Orchestration**: Stream responses from Gemini and Claude models through a unified API.
- **Tool Execution Engine**: Built-in system tools for terminal command execution, web fetching, and file operations.
- **Failover Routing**: Automatically falls back to secondary providers if rate limits or network errors occur.
- **SSE Streaming**: Full Server-Sent Events (SSE) streaming support for low-latency client rendering.

## Architecture

```
Client (Web / CLI)
       │
       ▼
[ FastAPI Gateway :8000 ]
       ├── /v1/chat/completions (SSE Stream)
       ├── /v1/tools/execute    (Safe Sandboxed Tools)
       └── /v1/models           (Provider Health & Quota)
       │
       ├── Provider 1: Google Gemini (Primary)
       └── Provider 2: Anthropic Claude (Fallback)
```

## Quick Start

### 1. Installation

```bash
git clone https://github.com/4techno/ai-chat-assistant.git
cd ai-chat-assistant
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your API keys:

```env
PORT=8000
GEMINI_API_KEY=your_gemini_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
DEFAULT_MODEL=gemini-2.0-flash
FALLBACK_MODEL=claude-3-5-haiku
```

### 3. Run the Gateway

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

## API Reference

### `POST /v1/chat`

Send a conversational query to the gateway:

```json
{
  "model": "gemini-2.0-flash",
  "messages": [
    {"role": "user", "content": "Explain inverse kinematics for a 4-axis arm."}
  ],
  "stream": true
}
```

## License

MIT License. Open to contributions and enhancements.
