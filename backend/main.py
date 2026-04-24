"""
main.py — Pura Support Agent: FastAPI backend

Phase 1 / CAP-3.S-1 will replace the mock stream below with a real Groq
LLM + ChromaDB RAG pipeline. For now, POST /chat returns a fake chunked
response word-by-word so the frontend streaming logic can be fully validated
without an LLM API key.

Run:
    uvicorn main:app --reload
"""

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="Pura Support Agent")

# Allow the Vite dev server to reach this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str


# --- Mock streaming response (replaced in CAP-3.S-1) ---

MOCK_RESPONSE = (
    "Thanks for reaching out! I can help you with that. "
    "Please make sure your Pura device is plugged in and within range of your 2.4 GHz Wi-Fi network. "
    "Open the Pura app, tap 'Add Device', and follow the on-screen steps. "
    "Let me know if you run into any issues!"
)


async def stream_mock_response(message: str):
    """Yield the mock response one word at a time with a short delay.

    The `message` parameter is accepted so the signature matches what
    the real Groq pipeline will expect in CAP-3.S-1.
    """
    _ = message  # will be used in CAP-3.S-1
    words = MOCK_RESPONSE.split(" ")
    for i, word in enumerate(words):
        # Re-join with space except before the first word
        chunk = word if i == 0 else f" {word}"
        yield chunk
        await asyncio.sleep(0.04)  # ~25 tokens/sec — realistic streaming feel


@app.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        stream_mock_response(request.message),
        media_type="text/plain",
    )
