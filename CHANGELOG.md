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

- `backend/requirements.txt` — added `fastapi`, `uvicorn[standard]`

#### RAG Retrieval Layer (CAP-1.S-2 — SUH-7)

- `backend/retrieval.py` — `retrieve(query, top_k=3)` function
  - Embeds query with `BAAI/bge-small-en-v1.5` (same model as `ingest.py` — model parity is critical for correct similarity scores)
  - Queries `pura_help_center` ChromaDB collection directly via `collection.query()`
  - Returns `list[dict]` with `text`, `article_title`, `source_filename`, `distance`
  - Returns `[]` for empty or whitespace-only queries — no exception
  - Model and ChromaDB client are module-level singletons — loaded once at import, not per call
  - Runnable standalone: `python retrieval.py "How do I set up my Pura Mini?"`
  - Validated: **8/10 accuracy** (gate ≥7/10 ✅), **max 301ms latency** (gate <500ms ✅), avg 90ms

#### Groq LLM Streaming (CAP-3.S-1 — SUH-9)

- `backend/main.py` — FastAPI server, now live (replaces mock from SUH-6)
  - `POST /chat` streams real responses from Groq `llama-3.3-70b-versatile` via `AsyncGroq`
  - System prompt: Pura brand identity + on-topic guard
  - Fails fast at startup if `GROQ_API_KEY` is missing
  - `groq.APIError` caught in the stream generator — yields user-facing message, never a raw 500
  - CORS open for `http://localhost:5173`
  - Run: `uvicorn main:app --reload`

- `backend/requirements.txt` — added `groq`

- `backend/.env.example` — added `GROQ_API_KEY=your_key_here`

#### RAG Grounding (CAP-3.S-2 — SUH-10)

- `backend/main.py` — updated to inject Help Center context before every Groq call
  - `retrieve(message, top_k=3)` called before Groq; chunks with `distance ≥ 1.0` filtered out
  - `build_system_prompt(chunks)` injects a `### CONTEXT ### ... ### END CONTEXT ###` block with retrieved chunk texts
  - LLM instructed to answer only from context; falls back to escalation offer when context is empty
  - Off-topic deflection preserved from CAP-3.S-1
  - Validated: **10/10 queries grounded** in KB content (gate ≥8/10 ✅); no hallucination observed

#### Conversation Memory (CAP-3.S-3 — SUH-11)

- `backend/main.py` — history now passed to Groq with every request
  - New `HistoryItem` Pydantic model: `{ role: "user"|"assistant", content: str }`
  - `ChatRequest.history: list[HistoryItem] | None = None` — optional; single-turn curl requests unchanged
  - `MAX_HISTORY_TURNS = 6` constant caps token growth (Groq free tier: 6,000 tokens/min)
  - Groq messages list: `[system_with_rag_context, ...last_6_history_turns, current_user_message]`

- `frontend/src/hooks/useChat.ts` — sends accumulated history with every `POST /chat`
  - History snapshot captured **before** appending new user message to state (prevents double-sending current turn)
  - Maps `"agent"` → `"assistant"` for Groq compatibility; strips internal `id` field; filters empty placeholders
  - Validated: 5-turn test — device context carried correctly across all turns (e.g. "How long does its battery last?" resolved to Pura Car Pro without re-stating the device)

#### Troubleshooting Wizard Mode (CAP-4.S-1 — SUH-12)

- `backend/main.py` — `BASE_PROMPT` extended with `## Troubleshooting Mode` instructions
  - Detects troubleshooting intent from natural language: "won't connect", "not working", "blinking light", "no scent", "won't pair", "won't charge", and related phrases
  - **Device-first rule**: if model is unknown, asks "Which Pura model do you have?" before any diagnosis
  - **One-question rule**: asks at most one clarifying question before providing steps — prevents multi-question interrogation
  - **Numbered steps**: once model and issue are clear, delivers concise numbered steps grounded in RAG context
  - Covers 5 issue categories: Wi-Fi/connectivity, pairing/detection, no scent/weak scent, LED abnormalities, battery/power (Car Pro/Car)
  - Validated: 5/5 categories pass ≥4/5 accuracy gate; multi-turn wizard confirmed end-to-end in browser
  - No new endpoints or frontend changes — prompt engineering only

#### Inline Image Links in Troubleshooting / Setup (CAP-4.S-3 — SUH-13)

- `backend/data/help_center/pura-mini-setup.md` — setup overview diagram added
- `backend/data/help_center/pura-mini-troubleshooting.md` — reset button image (inline with reset step) + LED indicator chart
- `backend/data/help_center/pura-car-pro-setup.md` — setup overview diagram + charging port image
- `backend/main.py` — prompt instruction added: LLM must include image markdown links verbatim inline with steps (without this instruction the LLM paraphrases them away)
- **Note:** Current images are `placehold.co` placeholders — replace with real Pura asset URLs and re-run `python ingest.py` when available

#### Changed

- `.gitignore` — `backend/data/help_center/` removed from ignore list; KB articles are authored content and should be tracked. Only `backend/data/chroma/` (generated vector store) remains excluded. All 29 Help Center articles are now committed to the repo.

#### Escalation Detection + Transcript (CAP-5.S-1 + CAP-5.S-2 — SUH-14 + SUH-15)

- `backend/main.py` — `BASE_PROMPT` extended with `## Escalation` section
  - **Immediate triggers**: "that didn't help", "still not working", "I want to talk to a person", "contact support", and close variants → escalates on the next response
  - **Proactive escalation**: if 2+ prior turns on the same unresolved issue are in history, agent escalates rather than attempting another answer
  - **Escalation message**: `"I wasn't able to resolve this — would you like me to connect you with the Pura support team?"`
  - **Support Summary block** always included on escalation:
    ```
    ---
    Support Summary
    Issue: <one-line summary>
    Steps tried: <bullet list>
    Status: Unresolved
    Contact: support@pura.com or pura.com/help
    ---
    ```

#### Conversation Logging to SQLite (CAP-6.S-1 — SUH-16)

- `backend/db.py` (new) — SQLite logging module
  - `init_db()` — creates `conversations` table and parent directories on first import; no manual setup needed
  - `log_turn(session_id, role, message)` — writes one row with ISO timestamp
  - Schema: `id` (PK), `session_id`, `timestamp`, `role` ("user"|"agent"), `message`
  - `DB_PATH` from env; default `./data/conversations.db`

- `backend/main.py` — logging wired into the stream generator
  - `ChatRequest` accepts optional `session_id: str | None`
  - Response tokens accumulated during streaming; both user message and agent response logged in `finally` after stream closes — never during, so streaming is unblocked
  - If `session_id` is absent, logging is silently skipped (backward-compatible)

- `frontend/src/hooks/useChat.ts` — session ID generated on mount
  - `sessionId = useRef(crypto.randomUUID())` — stable UUID for the conversation lifetime
  - Sent as `session_id` in every `POST /chat` body

- `backend/.env.example` — `DB_PATH=./data/conversations.db` added
- `.gitignore` — `backend/data/conversations.db` excluded (generated file)

#### Plans

- `docs/plans/suh-5-ingest-plan.md` — completed (100%)
- `docs/plans/suh-6-streaming-chat-plan.md` — completed (100%)
- `docs/plans/suh-7-retrieval-plan.md` — completed (100%)
- `docs/plans/suh-9-groq-streaming-plan.md` — completed (100%)
- `docs/plans/suh-10-rag-grounding-plan.md` — completed (100%)
- `docs/plans/suh-11-conversation-memory-plan.md` — completed (100%)
- `docs/plans/suh-12-troubleshooting-wizard-plan.md` — completed (100%)
- `docs/plans/suh-13-image-links-plan.md` — completed (100%)
- `docs/plans/suh-14-15-16-escalation-logging-plan.md` — completed (100%)
