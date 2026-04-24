# SUH-9 — Live Groq LLM Streaming via POST /chat

**Linear:** SUH-9 / CAP-3.S-1
**Overall Progress:** `95%`

## TLDR

Replace the mock streaming stub in `backend/main.py` with a real Groq API call (`llama-3.3-70b-versatile`). The frontend (`useChat.ts`) is unchanged — it already consumes any `text/plain` chunked response. This story wires the backend to a live LLM and adds a minimal system prompt + error handling.

## Critical Decisions

- **`AsyncGroq` client** — Groq's Python SDK ships async support natively; `AsyncGroq` + `async for` keeps FastAPI's event loop unblocked with no thread wrapping needed
- **System prompt minimal for this story** — Pura brand identity + on-topic guard only; RAG context injection is CAP-3.S-2 and must not be pre-empted here
- **Error caught inside the async generator** — `groq.APIError` is caught and a user-facing message is yielded before the stream closes, so the frontend never sees a raw 500

---

## Tasks

- [x] ✅ **Step 1: Add Groq dependency and API key config**
  - [x] ✅ Add `groq` to `backend/requirements.txt`
  - [x] ✅ Add `GROQ_API_KEY=your_key_here` to `backend/.env.example`
  - [x] ✅ Install into venv: `.venv/bin/pip install groq`
  - [x] ✅ Create `backend/.env` with real Groq API key (gitignored — never committed)

- [x] ✅ **Step 2: Rewrite `backend/main.py` with Groq streaming**
  - [x] ✅ Remove `MOCK_RESPONSE` constant and `stream_mock_response()` function
  - [x] ✅ Initialise `AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))` — fail fast at startup if key is missing
  - [x] ✅ Define `SYSTEM_PROMPT` — Pura support identity, warm tone, on-topic guard
  - [x] ✅ Implement `stream_groq_response(message: str)` async generator with `groq.APIError` handling
  - [x] ✅ Update `POST /chat` to call `stream_groq_response` — `StreamingResponse` and `media_type` unchanged

- [x] ✅ **Step 3: Smoke test end-to-end**
  - [x] ✅ Restart backend — clean startup, no errors
  - [x] ✅ "How do I set up my Pura Mini?" → real Groq response with numbered steps ✅
  - [x] ✅ "What is the capital of France?" → `"I'm here to help with Pura products only."` ✅
  - [ ] 🟥 Visual browser test: open `http://localhost:5173`, confirm streaming renders token-by-token in the widget
