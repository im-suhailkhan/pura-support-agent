# Pura Support Agent

An AI-powered customer support agent for Pura — the smart home fragrance brand. Ask it anything about your Pura device in plain English: setup, troubleshooting, fragrance vials, features. It retrieves answers from Pura's Help Center content, guides you through problems step-by-step, and escalates to a human with a conversation summary when it can't resolve an issue.

**Built by Suhail Khan (PM) · Phase 1 MVP**

---

## Demo

Ask it anything:
- *"How do I set up my Pura Mini?"* → setup video + numbered steps + image
- *"My device won't connect"* → asks which model → asks one clarifying question → numbered troubleshooting steps
- *"What is the battery life of the Pura Car Pro?"* → exact spec from Help Center
- *"I want to talk to a person"* → escalation message + pre-filled support summary

---

## Stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI (Python) |
| LLM | Groq — Llama 3.3 70B (free tier) |
| Embeddings | `BAAI/bge-small-en-v1.5` (local, no API cost) |
| Vector Store | ChromaDB (local, persistent) |
| RAG Framework | LlamaIndex |
| Database | SQLite (conversation logging) |

---

## Running Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- A free [Groq API key](https://console.groq.com)

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Add your GROQ_API_KEY to .env

# Ingest Help Center articles into ChromaDB
python ingest.py

# Start the API server
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`. Open it and start chatting.

---

## How It Works

```
User message
    │
    ▼
retrieve(query, top_k=3)          ← ChromaDB similarity search (~90ms)
    │
    ▼
build_system_prompt(chunks)       ← inject Help Center context
    │
    ▼
Groq Llama 3.3 70B (streaming)   ← grounded answer, token-by-token
    │
    ▼
useChat hook (ReadableStream)     ← renders in-place as stream arrives
    │
    ▼
log_turn() → SQLite               ← logged after stream closes (non-blocking)
```

**RAG grounding:** retrieved chunks are injected into the system prompt as a `### CONTEXT ###` block. The LLM is instructed to answer only from that context — verified at 10/10 accuracy across test queries, zero hallucination observed.

---

## Features (Phase 1)

- **RAG pipeline** — 29 Help Center articles (5 products × 5 topics) chunked, embedded locally, and stored in ChromaDB. Idempotent ingestion — re-running never duplicates chunks.
- **Streaming chat UI** — message appears instantly; agent reply streams token-by-token.
- **Conversation memory** — last 6 turns sent with every request so follow-up questions resolve without repeating context.
- **Troubleshooting wizard** — detects device problems, asks which model first, asks one clarifying question, delivers numbered steps.
- **Inline image links** — setup diagrams and reset button images surface alongside relevant steps.
- **Escalation path** — detects when it can't resolve an issue; generates a structured Support Summary (issue, steps tried, contact) for handoff to the support team.
- **Conversation logging** — every turn saved to SQLite with session ID, role, and timestamp.

---

## Knowledge Base

| Product | Setup | Features | Troubleshooting | FAQ | Cover |
|---|---|---|---|---|---|
| Pura Mini™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Plus™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura 3™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Car Pro™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Car™ | ✅ | ✅ | ✅ | ✅ | ✅ |

Articles live in `backend/data/help_center/`. To add or update content, edit the markdown files and re-run `python ingest.py`.

---

## Viewing Conversation Logs

```bash
# Terminal
sqlite3 -column -header backend/data/conversations.db \
  "SELECT session_id, timestamp, role, message FROM conversations ORDER BY id;"

# Or open backend/data/conversations.db in DB Browser for SQLite (GUI)
```

---

## Project Structure

```
pura-support-agent/
├── backend/
│   ├── main.py           # FastAPI server — RAG + Groq streaming + logging
│   ├── retrieval.py      # retrieve(query, top_k) — ChromaDB vector search
│   ├── ingest.py         # Help Center → ChromaDB ingestion pipeline
│   ├── db.py             # SQLite conversation logging
│   ├── requirements.txt
│   ├── .env.example
│   └── data/
│       └── help_center/  # 29 KB articles (markdown)
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── ChatWidget.tsx    # Chat panel UI
│       │   └── MessageBubble.tsx
│       └── hooks/
│           └── useChat.ts        # Streaming, history, session ID
└── docs/
    ├── pura-light-prd.md
    ├── roadmap-pura-support-agent-2026-04-23.md
    ├── phase-1-plan-pura-support-agent.md
    ├── showcase-document.md       # Full process walkthrough
    └── plans/                     # Per-story implementation plans
```

---

## Roadmap

| Phase | Theme | Status |
|---|---|---|
| Phase 1 — Know & Guide | Informational + troubleshooting, no auth | ✅ Complete |
| Phase 2 — Serve & Transact | Auth + Shopify integration, order/subscription actions | Planned |
| Phase 3 — Measure & Refine | CS analytics dashboard, ticket deflection measurement | Planned |

See [docs/roadmap-pura-support-agent-2026-04-23.md](docs/roadmap-pura-support-agent-2026-04-23.md) for full phase definitions and gate criteria.

---

## Docs

- [PRD](docs/pura-light-prd.md)
- [Roadmap](docs/roadmap-pura-support-agent-2026-04-23.md)
- [Phase 1 Plan](docs/phase-1-plan-pura-support-agent.md)
- [Showcase Document](docs/showcase-document.md)
- [Changelog](CHANGELOG.md)
