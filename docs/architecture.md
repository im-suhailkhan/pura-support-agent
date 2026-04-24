# Architecture: Pura Support Agent
**Last updated:** 2026-04-23
**Scope:** Phase 1 — local development / dummy frontend + backend
**Status:** Decided

---

## Stack

| Layer | Choice | Notes |
|---|---|---|
| Frontend | React + Vite | Dummy chat UI shell, local dev only |
| Styling | Tailwind CSS | |
| Backend | FastAPI (Python) | Streaming support, AI/RAG ecosystem |
| LLM | Groq API — Llama 3.3 70B | Free tier; swap model if rate limited |
| Embeddings | sentence-transformers `BAAI/bge-small-en-v1.5` | Runs locally, no API cost |
| Vector Store | ChromaDB | Local, persists to disk. Swap to pgvector/Pinecone for prod |
| Database | SQLite | Conversation logging. Swap to Postgres/Supabase for prod |
| RAG Framework | LlamaIndex (open-source core) | |
| Testing | Pytest (backend) + Vitest (frontend) | |

---

## Phase 1 — specific decisions

- **Auth:** None — Phase 1 is unauthenticated
- **Help Center sync:** Manual ingestion for Phase 1 (file drop); auto-sync on article publish is Phase 1 stretch
- **Job queue:** Not needed in Phase 1
- **Caching:** Not needed in Phase 1 — revisit if P95 misses 2s target
- **External APIs:** Groq API only — no Shopify, no auth provider

---

## Deferred to later phases

| Decision | Phase |
|---|---|
| Auth strategy (Supabase Auth or SSO) | Phase 2 |
| Shopify API integration | Phase 2 |
| Prod vector store (pgvector / Pinecone) | Phase 2+ |
| Prod database (Postgres / Supabase) | Phase 2+ |
| Ticketing system API (Zendesk / Gorgias) | Phase 3 |
| Deployment / hosting | Post-Phase 1 |
