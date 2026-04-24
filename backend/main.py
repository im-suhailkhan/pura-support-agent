"""
main.py — Pura Support Agent: FastAPI backend

CAP-3.S-2: POST /chat now retrieves top-3 relevant Help Center chunks from
ChromaDB before calling Groq. Chunks are injected into the system prompt as
a ### CONTEXT ### block, grounding the LLM in Pura's actual documentation.

Next:
  CAP-3.S-3 — include last N conversation turns for multi-turn memory

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

from retrieval import retrieve  # SUH-7: validated at 8/10 accuracy, ~90ms avg

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

# Distances ≥ 1.0 indicate the chunk is too dissimilar to be useful context.
# Calibrated from SUH-7: on-topic queries return ~0.5–0.8; off-topic ~1.17.
RELEVANCE_THRESHOLD = 1.0

BASE_PROMPT = (
    "You are a friendly, knowledgeable support agent for Pura, a premium smart home "
    "fragrance brand. Help customers with questions about their Pura devices "
    "(Pura Mini, Pura Plus, Pura 3, Pura Car Pro, Pura Car), fragrance vials, "
    "setup, troubleshooting, and general product information. "
    "Be warm, concise, and solution-focused — like a Pura brand expert, not a generic bot. "
    "If a question is unrelated to Pura products, politely say: "
    "'I'm here to help with Pura products only. Is there something about your device or fragrance I can assist with?'"
)


def build_system_prompt(chunks: list[dict]) -> str:
    """Build a context-aware system prompt from retrieved Help Center chunks.

    With context: instructs the LLM to answer only from the provided chunks.
    Without context: instructs the LLM to offer escalation instead of guessing.
    """
    if not chunks:
        return (
            BASE_PROMPT
            + "\n\n"
            + "If you cannot find a clear answer from your knowledge of Pura products, "
            + "say: \"I don't have information on that — would you like me to connect "
            + "you with the support team?\""
        )

    context_block = "\n---\n".join(
        f"[{c['article_title']}]\n{c['text']}" for c in chunks
    )

    return (
        BASE_PROMPT
        + "\n\n### CONTEXT ###\n"
        + context_block
        + "\n### END CONTEXT ###\n\n"
        + "Answer the customer's question using ONLY the information in the CONTEXT above. "
        + "If the context does not contain enough information to answer confidently, say: "
        + "\"I don't have information on that — would you like me to connect you with the support team?\" "
        + "Do not use knowledge outside the provided context."
    )


class ChatRequest(BaseModel):
    message: str


async def stream_groq_response(message: str):
    """Retrieve relevant Help Center chunks, then stream a grounded Groq response.

    Flow:
    1. Retrieve top-3 chunks from ChromaDB (retrieval.py).
    2. Filter to chunks with distance < RELEVANCE_THRESHOLD.
    3. Build a context-aware system prompt.
    4. Stream Groq response token-by-token.
    """
    chunks = retrieve(message, top_k=3)
    relevant_chunks = [c for c in chunks if c["distance"] < RELEVANCE_THRESHOLD]
    system_prompt = build_system_prompt(relevant_chunks)

    try:
        stream = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
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
