# Changelog

All notable changes to this project will be documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Unreleased]

### Added

#### RAG Knowledge Base (CAP-1.S-1 — SUH-5)

- `backend/ingest.py` — CLI script to ingest Help Center articles into ChromaDB
  - Reads all `.md` and `.txt` files from `--docs-dir` (default: `./data/help_center`)
  - Chunks with `SentenceSplitter`: 512 tokens, 50-token overlap
  - Embeds locally via `BAAI/bge-small-en-v1.5` (no API cost)
  - Upserts into ChromaDB collection `pura_help_center` at `--chroma-path`
  - **Idempotent**: chunk IDs are `md5(source_filename:chunk_index)` — re-runs update, never duplicate
  - Each chunk carries metadata: `article_title`, `source_filename`
  - Prints `✓ X article(s) processed, Y chunk(s) stored in ChromaDB` on completion

- `backend/requirements.txt` — Python dependencies: `llama-index`, `llama-index-vector-stores-chroma`, `llama-index-embeddings-huggingface`, `chromadb`, `sentence-transformers`, `python-dotenv`

- `backend/.env.example` — documents `CHROMA_PATH` and `DOCS_DIR` env vars

- `backend/.gitignore` — excludes `data/chroma/`, `data/help_center/`, `.env`, `__pycache__/`, `.venv/`

#### Help Center Knowledge Base (25 articles)

Product × topic markdown files covering all 5 Pura devices across 5 support intents:

| Product | setup | features | troubleshooting | faq | cover replacement |
|---|---|---|---|---|---|
| Pura Mini™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Plus™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura 3™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Car Pro™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Car™ | ✅ | ✅ | ✅ | ✅ | ✅ |

All setup files include the global setup video URL. Troubleshooting files are product-specific.
Naming convention: `{product}-{topic}.md` (e.g. `pura-3-troubleshooting.md`).

> Note: 4 placeholder articles remain (`fragrance-subscription.md`, `how-to-use-the-pura-diffuser.md`, `returns-and-refunds.md`, `troubleshooting-connectivity.md`) — superseded by product-specific files; safe to delete.

#### Streaming Chat UI (CAP-2.S-1 + CAP-2.S-2 — SUH-6)

- `frontend/` — React + Vite + TypeScript project scaffolded with Tailwind CSS v4 (`@tailwindcss/vite`)

- `frontend/src/components/ChatWidget.tsx` — main chat panel
  - Fixed 420×600px card layout: purple header, scrollable message list, pinned input row
  - Empty state: `"Hi! Ask me anything about your Pura."`
  - Input focused on mount; Enter submits, Shift+Enter inserts newline
  - Input + Send button disabled while streaming; re-enabled on completion
  - Auto-scrolls to latest message on every state update

- `frontend/src/components/MessageBubble.tsx` — single message bubble
  - User messages: right-aligned, purple background
  - Agent messages: left-aligned, white card with border

- `frontend/src/hooks/useChat.ts` — all message state and streaming logic
  - `sendMessage(text)`: appends user message immediately, then fetches `POST /chat`
  - Reads response body as `ReadableStream`; updates agent bubble in-place per chunk (no new bubble per token)
  - On error: sets agent message to `"Something went wrong. Please try again."`

- `backend/main.py` — FastAPI server (mock phase; replaced in CAP-3.S-1)
  - `POST /chat` accepts `{ message: string }`, streams a fixed response word-by-word at ~40ms/token
  - CORS open for `http://localhost:5173`
  - Run: `uvicorn main:app --reload`

- `backend/requirements.txt` — added `fastapi`, `uvicorn[standard]`

#### RAG Retrieval Layer (CAP-1.S-2 — SUH-7)

- `backend/retrieval.py` — `retrieve(query, top_k=3)` function
  - Embeds query with `BAAI/bge-small-en-v1.5` (same model as `ingest.py` — model parity is critical for correct similarity scores)
  - Queries `pura_help_center` ChromaDB collection directly via `collection.query()`
  - Returns `list[dict]` with `text`, `article_title`, `source_filename`, `distance`
  - Returns `[]` for empty or whitespace-only queries — no exception
  - Off-topic queries return low-relevance results (dist ≈ 1.17) without crashing
  - Model and ChromaDB client are module-level singletons — loaded once at import, not per call
  - Runnable standalone: `python retrieval.py "How do I set up my Pura Mini?"`
  - Validated: **8/10 accuracy** (gate ≥7/10 ✅), **max 301ms latency** (gate <500ms ✅), avg 90ms

#### Plans

- `docs/plans/suh-5-ingest-plan.md` — completed (100%)
- `docs/plans/suh-6-streaming-chat-plan.md` — completed (95% — pending browser sign-off)
- `docs/plans/suh-7-retrieval-plan.md` — completed (100%)
