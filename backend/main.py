"""
main.py — Pura Support Agent: FastAPI backend

CAP-3.S-1: POST /chat now streams a real response from Groq (llama-3.3-70b-versatile).
The frontend (useChat.ts) is unchanged — it consumes any text/plain chunked stream.

Next:
  CAP-3.S-2 — inject top-3 ChromaDB chunks as context before the LLM call
  CAP-3.S-3 — include last N conversation turns for memory

Run:
    uvicorn main:app --reload
"""

import os
import sys

import groq as groq_lib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from groq import AsyncGroq
from pydantic import BaseModel

load_dotenv()

_api_key = os.getenv("GROQ_API_KEY")
if not _api_key:
    print("[error] GROQ_API_KEY is not set. Add it to backend/.env", file=sys.stderr)
    sys.exit(1)

app = FastAPI(title="Pura Support Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

client = AsyncGroq(api_key=_api_key)

MODEL = "llama-3.3-70b-versatile"

# Minimal brand prompt for CAP-3.S-1.
# RAG context (retrieved Help Center chunks) is injected here in CAP-3.S-2.
SYSTEM_PROMPT = (
    "You are a friendly, knowledgeable support agent for Pura, a premium smart home "
    "fragrance brand. Help customers with questions about their Pura devices "
    "(Pura Mini, Pura Plus, Pura 3, Pura Car Pro, Pura Car), fragrance vials, "
    "setup, troubleshooting, and general product information. "
    "Be warm, concise, and solution-focused — like a Pura brand expert, not a generic bot. "
    "If a question is unrelated to Pura products, politely say: "
    "'I'm here to help with Pura products only. Is there something about your device or fragrance I can assist with?'"
)


class ChatRequest(BaseModel):
    message: str


async def stream_groq_response(message: str):
    """Stream a Groq LLM response token-by-token.

    Yields raw text chunks as they arrive from the API.
    On API error, yields a user-facing message and exits cleanly
    so the frontend always receives a complete (if brief) response.
    """
    try:
        stream = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            stream=True,
        )
        async for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            if token:
                yield token
    except groq_lib.APIError as e:
        yield f"Something went wrong. Please try again. ({type(e).__name__})"


@app.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        stream_groq_response(request.message),
        media_type="text/plain",
    )
