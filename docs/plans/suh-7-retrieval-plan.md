# SUH-7 — RAG Retrieval: Query → Top-3 Help Center Chunks

**Linear:** SUH-7 / CAP-1.S-2
**Overall Progress:** `100% ✅`

## TLDR

Build `backend/retrieval.py`: a single `retrieve(query, top_k=3)` function that embeds a natural language query and returns the top-k most relevant Help Center chunks from ChromaDB. Validates the ≥7/10 accuracy gate and <500ms latency requirement against 10 defined test queries. Unblocks CAP-3.S-2 (grounded LLM answers).

## Critical Decisions

- **Direct `collection.query()` over LlamaIndex retriever** — retrieval only needs embed + similarity search; no need to reload the full LlamaIndex index machinery. Direct ChromaDB call is simpler and mirrors the `ingest.py` client pattern
- **Share constants with `ingest.py`** — same `EMBEDDING_MODEL`, `CHROMA_COLLECTION`, and `CHROMA_PATH` env var; a model mismatch between ingest and retrieval would silently break relevance
- **Return `list[dict]`** with keys `text`, `article_title`, `source_filename` — this is the wire format `main.py` will consume in CAP-3.S-2; agreeing on it now avoids a refactor later

---

## Tasks

- [x] ✅ **Step 1: Write `backend/retrieval.py`**
  - [x] ✅ Load `CHROMA_PATH` from env (same default as `ingest.py`: `./data/chroma`)
  - [x] ✅ Initialise `HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")` and `chromadb.PersistentClient` — same constants as `ingest.py`
  - [x] ✅ Implement `retrieve(query: str, top_k: int = 3) -> list[dict]`:
    - Embed `query` → query vector
    - Call `collection.query(query_embeddings=[vector], n_results=top_k, include=["documents", "metadatas", "distances"])`
    - Return `[{"text": ..., "article_title": ..., "source_filename": ..., "distance": ...}]`
    - Return `[]` if the collection is empty or query is blank

- [x] ✅ **Step 2: Validate accuracy and latency**
  - [x] ✅ Run all 10 test queries — results:
    1. ✅ "How do I set up my Pura Mini?" → `pura-mini-setup`
    2. ❌ "My Pura 3 won't connect to Wi-Fi" → `troubleshooting-connectivity` (stale placeholder outranked `pura-3-troubleshooting`)
    3. ✅ "What is the battery life of the Pura Car Pro?" → `pura-car-pro-faq`
    4. ✅ "How do I replace the cover on my Pura Plus?" → `pura-plus-cover-replacement`
    5. ✅ "How long does a fragrance vial last?" → `pura-mini-faq`
    6. ✅ "Pura Car not diffusing" → `pura-car-pro-troubleshooting`
    7. ✅ "Features of the Pura 3" → `pura-3-features`
    8. ❌ "Pura Mini FAQ" → `pura-mini-features` (FAQ landed #2; data quality, not retrieval bug)
    9. ✅ "How do I return my diffuser?" → `returns-and-refunds`
    10. ✅ "Pura Car Pro motion detection not working" → `pura-car-pro-troubleshooting`
  - [x] ✅ Accuracy: **8/10** (gate: ≥7/10) ✅
  - [x] ✅ Latency: **max 301ms, avg 90ms** (gate: <500ms) ✅
  - Note: 2 misses are content/data issues — deleting stale placeholder articles would bring accuracy to ≥9/10

- [x] ✅ **Step 3: Verify edge case handling**
  - [x] ✅ Off-topic query (`"what is the capital of France?"`) → returns 3 low-relevance chunks (dist≈1.17), no crash
  - [x] ✅ Empty string `""` → returns `[]`, no exception
  - [x] ✅ Whitespace-only `"   "` → returns `[]`, no exception
