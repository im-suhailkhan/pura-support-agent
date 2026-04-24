# SUH-5 — Ingestion Script: Help Center → ChromaDB

**Overall Progress:** `100% ✅`

## TLDR

Build `backend/ingest.py`: a standalone CLI script that reads Pura Help Center markdown/text files, chunks them (512 tokens, 50-token overlap), embeds each chunk locally with `bge-small-en-v1.5`, and upserts into a local ChromaDB collection. Re-runnable without duplicating chunks. Unblocks all RAG-dependent stories.

## Critical Decisions

- **LlamaIndex for chunking + ChromaDB integration** — already in stack; handles token-aware splitting and ChromaDB upsert via `ChromaVectorStore`
- **`BAAI/bge-small-en-v1.5` embeddings are local** — no API cost, wraps into LlamaIndex via `HuggingFaceEmbedding`
- **Upsert via stable doc IDs** — each chunk ID is derived from `source_filename + chunk_index`; LlamaIndex's `VectorStoreIndex` with `store_nodes_override` handles upsert cleanly
- **ChromaDB path from `.env`** — `CHROMA_PATH` (default `./data/chroma`); `.env.example` documents it
- **No LLM needed** — ingestion is embed-only; Groq key not required for this script

---

## Tasks

- [x] ✅ **Step 1: Scaffold backend directory and dependencies**
  - [x] ✅ Create `backend/` directory structure: `data/help_center/`, `data/chroma/`
  - [x] ✅ Create `backend/requirements.txt` with: `llama-index`, `llama-index-vector-stores-chroma`, `llama-index-embeddings-huggingface`, `chromadb`, `sentence-transformers`, `python-dotenv`
  - [x] ✅ Create `backend/.env.example` with `CHROMA_PATH=./data/chroma` and `DOCS_DIR=./data/help_center`
  - [x] ✅ Create `backend/.gitignore` ignoring `data/chroma/`, `data/help_center/`, `.env`

- [x] ✅ **Step 2: Write the ingestion script**
  - [x] ✅ Create `backend/ingest.py` with `argparse` CLI: `--docs-dir` (default from `.env`), `--chroma-path` (default from `.env`)
  - [x] ✅ Load all `.md` and `.txt` files from `--docs-dir` using LlamaIndex `SimpleDirectoryReader`; attach `article_title` (filename stem) and `source_filename` as metadata
  - [x] ✅ Configure `SentenceSplitter` with `chunk_size=512`, `chunk_overlap=50`
  - [x] ✅ Configure `HuggingFaceEmbedding` with model `BAAI/bge-small-en-v1.5`
  - [x] ✅ Initialise ChromaDB client (persistent, at `--chroma-path`); get-or-create collection `pura_help_center`
  - [x] ✅ Build `VectorStoreIndex` from documents — LlamaIndex upserts by node ID, preventing duplicates
  - [x] ✅ Print completion summary: `✓ X articles processed, Y chunks stored in ChromaDB`

- [x] ✅ **Step 3: Verify idempotency**
  - [x] ✅ Run the script twice against a sample folder; confirm chunk count does not double on second run
  - [x] ✅ Add one new file, re-run; confirm only the new file's chunks are added

- [x] ✅ **Step 4: Smoke test with sample content**
  - [x] ✅ Drop 2–3 representative Pura Help Center articles into `data/help_center/`
  - [x] ✅ Run `python ingest.py` end-to-end; confirm no errors and summary prints correctly
  - [x] ✅ Open a Python REPL and do a raw ChromaDB query to confirm chunks + metadata are present
