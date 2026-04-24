"""
retrieval.py — RAG retrieval layer for the Pura Support Agent

Embeds a natural language query using the same model used at ingest time
(BAAI/bge-small-en-v1.5) and returns the top-k most relevant Help Center
chunks from ChromaDB.

Keeping the embedding model identical to ingest.py is critical: a mismatch
would produce vectors in different spaces and silently destroy retrieval quality.

Usage (standalone test):
    python retrieval.py "How do I set up my Pura Mini?"
"""

import os
import sys
import time
from dotenv import load_dotenv

import chromadb
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

# Must match ingest.py exactly — any drift silently breaks relevance
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
CHROMA_COLLECTION = "pura_help_center"
CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/chroma")

# Module-level singletons — initialised once, reused across calls.
# Loading the embedding model is expensive (~1s); we do it at import time
# so individual retrieve() calls are fast.
_embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
_chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _chroma_client.get_or_create_collection(CHROMA_COLLECTION)


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """Return the top-k most relevant Help Center chunks for a query.

    Args:
        query:  Natural language query string.
        top_k:  Number of results to return (default 3).

    Returns:
        List of dicts, each containing:
            text            — chunk content
            article_title   — human-readable article name (filename stem)
            source_filename — original markdown filename
            distance        — cosine distance (lower = more similar)
        Returns [] if the collection is empty or query is blank.
    """
    if not query.strip():
        return []

    # Embed the query into the same vector space used at ingest time
    query_vector = _embed_model.get_query_embedding(query)

    results = _collection.query(
        query_embeddings=[query_vector],
        n_results=min(top_k, _collection.count() or 1),
        include=["documents", "metadatas", "distances"],
    )

    # Unpack parallel lists returned by ChromaDB into a flat list of dicts
    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append(
            {
                "text": text,
                "article_title": meta.get("article_title", ""),
                "source_filename": meta.get("source_filename", ""),
                "distance": round(dist, 4),
            }
        )

    return chunks


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "How do I set up my Pura Mini?"
    print(f"Query: {query!r}\n")

    t0 = time.perf_counter()
    chunks = retrieve(query)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    for i, chunk in enumerate(chunks, 1):
        print(f"[{i}] {chunk['article_title']} ({chunk['source_filename']})  dist={chunk['distance']}")
        print(f"    {chunk['text'][:120].strip()!r}")
        print()

    print(f"Latency: {elapsed_ms:.1f}ms  |  Results: {len(chunks)}")
