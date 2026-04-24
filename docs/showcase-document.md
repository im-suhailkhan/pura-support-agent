# Pura Support Agent — Product Showcase

**Built by:** Suhail Khan  
**Role:** Product Manager  
**GitHub:** https://github.com/im-suhailkhan/pura-support-agent  
**Linear (project board):** https://linear.app/suhails-personal/project/pura-support-agent-706e30f33a12  

---

## What I Built

A fully functional AI-powered customer support agent for Pura — the smart home fragrance brand. The agent answers product, setup, and troubleshooting questions in natural language, guides users through device problems step-by-step, remembers prior turns in the conversation, and offers a structured escalation path when it can't resolve an issue.

This is a complete Phase 1 MVP: knowledge base, streaming chat UI, RAG pipeline, conversation memory, troubleshooting wizard, escalation flow, and conversation logging — all shipped, tested, and documented.

---

## The Problem

Pura's support volume is high and repetitive. Customers wait hours or days for answers to questions that repeat constantly: device setup, Wi-Fi connectivity, fragrance vial life, subscription management. The existing Help Center is static and searchable only — it doesn't guide users through problems. Human agents are overwhelmed.

**North star:** 50–70% reduction in support tickets for the 13 core support topics within 90 days of launch.

---

## Process: From Brainstorming to Shipped Code

### 1. Opportunity Sizing & Ideation
Started with a structured ideation document mapping the gap between Pura's chatbot (click-tree navigation) and what a conversational AI agent could do. Identified the highest-value deflectable topics and validated that 60–80% of query volume is automatable based on ticket data.

### 2. PRD
Wrote a full PRD defining the problem, user personas (Sarah — a first-time Pura customer), success metrics, scope (website-only MVP, no mobile), and explicit non-goals (no subscription cancellation via agent, no voice interface). The PRD locked the north star metric and set the phase gate criteria.

### 3. Roadmap (3 Phases)
Broke the product into three sequenced phases, each with its own assumption being tested:

| Phase | Theme | Assumption |
|---|---|---|
| Phase 1 — Know & Guide | Informational + troubleshooting, no auth | Help Center content is accurate enough to power ≥80% RAG accuracy |
| Phase 2 — Serve & Transact | Auth + Shopify integration, order/subscription actions | Shopify API is accessible and users trust the agent with account data |
| Phase 3 — Measure & Refine | CS analytics dashboard, deflection measurement | Combined resolution rate hits ≥85%, deflection ≥50% |

Each phase has a measurable go/no-go gate before the next begins.

### 4. Phase 1 Breakdown (Story Mapping)
Decomposed Phase 1 into 6 capabilities and 14 user stories, sequenced by dependency. Created Linear tickets for each story following a consistent format: user story, acceptance criteria, files to touch, effort, and dependencies.

### 5. Development Workflow (PM-Led Vibe Coding)
For each story: `/create-issue` (Linear ticket) → `/create-plan` (markdown implementation plan) → `/execute` (implementation) → `/document` (CHANGELOG). Every story is traceable from the Linear ticket through the plan document to the commit.

---

## Technical Architecture

| Layer | Choice | Rationale |
|---|---|---|
| Frontend | React + Vite + Tailwind CSS | Standard, fast to scaffold |
| Backend | FastAPI (Python) | Native async, streaming support |
| LLM | Groq — Llama 3.3 70B | Free tier, fast inference |
| Embeddings | BAAI/bge-small-en-v1.5 | Runs locally, no API cost |
| Vector Store | ChromaDB | Local persistence, simple to run |
| RAG Framework | LlamaIndex | Chunking + embedding pipeline |
| Database | SQLite | Conversation logging, zero setup |

---

## Phase 1: What Was Built (16 Linear Stories)

### Capability 1 — RAG Knowledge Base
- **SUH-5 (CAP-1.S-1):** Ingestion script — reads 29 Help Center markdown articles, chunks them (512 tokens, 50-token overlap), embeds locally, upserts to ChromaDB. Idempotent: re-running never duplicates chunks.
- **SUH-7 (CAP-1.S-2):** Retrieval layer — `retrieve(query, top_k=3)` returns relevant chunks in avg 90ms. Validated at 8/10 accuracy against 10 test queries.

### Capability 2 — Chat Widget UI
- **SUH-8 (CAP-2.S-1):** Chat widget shell — 420×600px fixed panel, welcome empty state, input focused on mount.
- **SUH-6 (CAP-2.S-2):** Streaming message interaction — user message appears instantly, agent reply streams token-by-token via Fetch ReadableStream. Input locked during streaming; auto-scrolls.

### Capability 3 — LLM + RAG Pipeline
- **SUH-9 (CAP-3.S-1):** Groq integration — POST /chat streams real Llama 3.3 70B responses. System prompt establishes Pura brand identity and on-topic guard.
- **SUH-10 (CAP-3.S-2):** RAG grounding — top-3 chunks injected into system prompt as `### CONTEXT ###` block. LLM instructed to answer only from context. Validated: 10/10 queries grounded in KB content, zero hallucination observed.
- **SUH-11 (CAP-3.S-3):** Conversation memory — last 6 turns sent with every request. Validated across a 5-turn conversation with correct device context carry-through.

### Capability 4 — Troubleshooting Wizard
- **SUH-12 (CAP-4.S-1):** Wizard mode — detects troubleshooting intent from natural language, asks for device model first, asks one clarifying question, then delivers numbered steps. Validated 5/5 categories at ≥4/5 phrasing accuracy.
- **SUH-13 (CAP-4.S-3):** Image links — inline placeholder images added to 3 KB articles (setup diagram, reset button, LED chart). Prompt instructs LLM to preserve image markdown verbatim.

### Capability 5 — Escalation Path
- **SUH-14 (CAP-5.S-1):** Escalation detection — fires immediately on "talk to a person", "that didn't help", etc. Proactively escalates after 2+ unresolved turns.
- **SUH-15 (CAP-5.S-2):** Escalation transcript — structured Support Summary block on every escalation (issue, steps tried, status, support@pura.com contact).

### Capability 6 — Conversation Logging
- **SUH-16 (CAP-6.S-1):** SQLite logging — every turn written to `conversations.db` after stream closes (non-blocking). Session ID generated via `crypto.randomUUID()` on the frontend, persisted across turns. Auto-creates DB on first run.

---

## Key Metrics (Phase 1 QA)

| Metric | Result | Gate |
|---|---|---|
| RAG grounding accuracy | 10/10 queries grounded in KB | ≥8/10 |
| Retrieval latency | avg 90ms, max 301ms | <500ms |
| Troubleshooting intent detection | 5/5 categories pass | ≥4/5 per category |
| Escalation trigger accuracy | Fires on all tested triggers | All explicit triggers |
| Zero hallucination | Confirmed across 10 test queries | No dangerous/wrong advice |

---

## Knowledge Base

29 articles across 5 products × 5 support topics:

| Product | Setup | Features | Troubleshooting | FAQ | Cover |
|---|---|---|---|---|---|
| Pura Mini™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Plus™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura 3™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Car Pro™ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pura Car™ | ✅ | ✅ | ✅ | ✅ | ✅ |

All setup articles include the Pura setup video link. Troubleshooting articles are product-specific with inline image links.

---

## What's Next (Phase 2 & 3 Roadmap)

**Phase 2 — Serve & Transact:** Add Shopify API integration and user auth so the agent can look up real order status, skip a shipment, and update a shipping address — all within the chat widget.

**Phase 3 — Measure & Refine:** CS analytics dashboard showing resolution rate per topic, escalation triggers, and CSAT by topic. Weekly RAG refinement workflow. Ticket deflection measurement integrated with Zendesk/Gorgias.

---

## Repository Structure

```
pura-support-agent/
├── backend/
│   ├── main.py          # FastAPI server — RAG + Groq streaming
│   ├── retrieval.py     # retrieve(query, top_k) — ChromaDB query
│   ├── ingest.py        # Help Center → ChromaDB ingestion pipeline
│   ├── db.py            # SQLite conversation logging
│   └── data/help_center/  # 29 KB articles (markdown)
├── frontend/
│   ├── src/components/
│   │   ├── ChatWidget.tsx   # Chat panel UI
│   │   └── MessageBubble.tsx
│   └── src/hooks/
│       └── useChat.ts    # Streaming fetch, history, session ID
└── docs/
    ├── pura-light-prd.md
    ├── roadmap-pura-support-agent.md
    ├── phase-1-plan-pura-support-agent.md
    └── plans/            # Per-story implementation plans (SUH-5 through SUH-16)
```
