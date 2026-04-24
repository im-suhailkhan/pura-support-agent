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

#### Plans

- `docs/plans/suh-5-ingest-plan.md` — completed (100%)
- `docs/plans/suh-6-streaming-chat-plan.md` — plan for CAP-2.S-2: streaming chat UI + mock backend stub
