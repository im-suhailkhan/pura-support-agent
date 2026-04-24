"""
main.py — Pura Support Agent: FastAPI backend

CAP-3.S-3: POST /chat now accepts an optional conversation history and
includes the last MAX_HISTORY_TURNS turns in the Groq messages list so
the agent can resolve follow-up questions without the user repeating context.

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

# Number of prior turns passed to Groq per request.
# Caps token growth on Groq's free tier (6,000 tokens/min).
MAX_HISTORY_TURNS = 6

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


class HistoryItem(BaseModel):
    role: str     # "user" or "assistant" (Groq-compatible values)
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[HistoryItem] | None = None  # optional — omitting keeps single-turn curl tests valid


async def stream_groq_response(message: str, history: list[HistoryItem]):
    """Retrieve Help Center context, prepend conversation history, stream Groq response.

    Messages sent to Groq: [system_with_context, ...last N history turns, current user message]
    """
    chunks = retrieve(message, top_k=3)
    relevant_chunks = [c for c in chunks if c["distance"] < RELEVANCE_THRESHOLD]
    system_prompt = build_system_prompt(relevant_chunks)

    # Cap history to avoid unbounded token growth; backend is the safety net even
    # if the frontend sends more turns than expected.
    history_messages = [
        {"role": h.role, "content": h.content}
        for h in history[-MAX_HISTORY_TURNS:]
    ]

    try:
        stream = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                *history_messages,
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
        stream_groq_response(request.message, request.history or []),
        media_type="text/plain",
    )
