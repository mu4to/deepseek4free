#!/usr/bin/env python3
"""
OpenAI-compatible server for deepseek4free.

Exposes DeepSeek's free web chat API as an OpenAI Chat Completions endpoint.
Designed to work with DeepSeek Harness (Custom model API provider).

Usage:
    1. Set DEEPSEEK_AUTH_TOKEN in .env (or environment)
    2. python openai_server.py
    3. In DeepSeek Harness → Base URL: http://127.0.0.1:8000/v1
"""

from __future__ import annotations

import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from dsk.api import DeepSeekAPI

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TOKEN = os.getenv("DEEPSEEK_AUTH_TOKEN", "").strip()
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

if not TOKEN:
    raise SystemExit(
        "ERROR: DEEPSEEK_AUTH_TOKEN is not set.\n"
        "Create a .env file with:\n"
        "  DEEPSEEK_AUTH_TOKEN=your_token_here\n"
        "Get the token from chat.deepseek.com → F12 → Application → Local Storage → userToken"
    )

app = FastAPI(
    title="deepseek4free OpenAI Proxy",
    description="Unofficial OpenAI-compatible proxy for DeepSeek web chat",
    version="1.0.0",
)

api = DeepSeekAPI(TOKEN)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class Message(BaseModel):
    role: str
    content: Optional[str] = None  # Harness sometimes sends null


class ChatCompletionRequest(BaseModel):
    model: str = "deepseek-chat"
    messages: List[Message]
    stream: bool = False
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def extract_prompt(messages: List[Message]) -> str:
    """Take the last non-empty user message. Harness can send huge histories with nulls."""
    valid = [m for m in messages if m.content and isinstance(m.content, str) and m.content.strip()]
    user_msgs = [m for m in valid if m.role == "user"]
    if not user_msgs:
        raise HTTPException(status_code=400, detail="No valid user message found")
    return user_msgs[-1].content.strip()


def is_thinking_model(model: str) -> bool:
    m = model.lower()
    return "reasoner" in m or "think" in m or "r1" in m


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/v1/models")
async def list_models():
    now = int(time.time())
    return {
        "object": "list",
        "data": [
            {
                "id": "deepseek-chat",
                "object": "model",
                "created": now,
                "owned_by": "deepseek4free",
            },
            {
                "id": "deepseek-reasoner",
                "object": "model",
                "created": now,
                "owned_by": "deepseek4free",
            },
        ],
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    prompt = extract_prompt(req.messages)
    thinking_enabled = is_thinking_model(req.model)

    try:
        chat_id = api.create_chat_session()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {e}")

    if req.stream:
        return StreamingResponse(
            stream_response(chat_id, prompt, thinking_enabled, req.model),
            media_type="text/event-stream",
        )
    return non_stream_response(chat_id, prompt, thinking_enabled, req.model)


def non_stream_response(chat_id: str, prompt: str, thinking_enabled: bool, model: str) -> Dict[str, Any]:
    full_text = ""
    try:
        for chunk in api.chat_completion(chat_id, prompt, thinking_enabled=thinking_enabled):
            if chunk.get("type") == "text" and chunk.get("content"):
                full_text += chunk["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": full_text},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


async def stream_response(chat_id: str, prompt: str, thinking_enabled: bool, model: str):
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())

    # role chunk
    first = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "choices": [{"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}],
    }
    yield f"data: {json.dumps(first)}\n\n"

    try:
        for chunk in api.chat_completion(chat_id, prompt, thinking_enabled=thinking_enabled):
            if chunk.get("type") == "text" and chunk.get("content"):
                data = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": chunk["content"]},
                            "finish_reason": None,
                        }
                    ],
                }
                yield f"data: {json.dumps(data)}\n\n"
    except Exception as e:
        err = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{"index": 0, "delta": {"content": f"\n[Error: {e}]"}, "finish_reason": "stop"}],
        }
        yield f"data: {json.dumps(err)}\n\n"

    # finish
    done = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }
    yield f"data: {json.dumps(done)}\n\n"
    yield "data: [DONE]\n\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"🚀 deepseek4free OpenAI server starting on http://{HOST}:{PORT}")
    print(f"👉 In DeepSeek Harness set Base URL to: http://{HOST}:{PORT}/v1")
    print(f"   Models: deepseek-chat | deepseek-reasoner")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
