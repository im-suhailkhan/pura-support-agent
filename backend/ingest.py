"""
ingest.py — Pura Help Center → ChromaDB ingestion pipeline

Reads markdown/text articles from a docs directory, splits them into
512-token chunks with 50-token overlap, embeds each chunk locally using
BAAI/bge-small-en-v1.5, and upserts into a persistent ChromaDB collection.

Re-running is safe: each chunk is assigned a deterministic ID derived from
(source_filename, per-file chunk index). ChromaDB upserts by ID so
re-running never duplicates chunks; only newly-added articles get new entries.

Usage:
    python ingest.py
    python ingest.py --docs-dir ./data/help_center --chroma-path ./data/chroma
"""

import argparse
import hashlib
import os
import sys
from collections import defaultdict
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
CHROMA_COLLECTION = "pura_help_center"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest Pura Help Center docs into ChromaDB."
    )
    parser.add_argument(
        "--docs-dir",
        default=os.getenv("DOCS_DIR", "./data/help_center"),
        help="Directory containing .md / .txt articles (default: $DOCS_DIR or ./data/help_center)",
    )
    parser.add_argument(
        "--chroma-path",
        default=os.getenv("CHROMA_PATH", "./data/chroma"),
        help="ChromaDB persistence directory (default: $CHROMA_PATH or ./data/chroma)",
    )
    return parser.parse_args()


def load_documents(docs_dir: str):
    """Load all .md and .txt files from docs_dir.

    Attaches article_title (filename stem) and source_filename as metadata
    so retrieval results can cite the originating article.
    """
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        print(f"[error] docs-dir not found: {docs_path.resolve()}", file=sys.stderr)
        sys.exit(1)

    files = list(docs_path.glob("*.md")) + list(docs_path.glob("*.txt"))
    if not files:
        print(
            f"[warn] No .md or .txt files found in {docs_path.resolve()}. "
            "Drop articles there and re-run.",
            file=sys.stderr,
        )
        sys.exit(0)

    reader = SimpleDirectoryReader(
        input_files=[str(f) for f in files],
        # Attach filename metadata to every document so chunks inherit it
        file_metadata=lambda path: {
            "article_title": Path(path).stem,
            "source_filename": Path(path).name,
        },
    )
    documents = reader.load_data()
    return documents, len(files)


def assign_stable_ids(nodes: list) -> list:
    """Replace LlamaIndex's random UUIDs with deterministic chunk IDs.

    ID format: md5(source_filename:chunk_index_within_file)
    This ensures re-runs upsert rather than duplicate existing chunks.
    New articles get new IDs that haven't been seen by ChromaDB before.
    """
    per_file_counter: dict[str, int] = defaultdict(int)
    for node in nodes:
        filename = node.metadata.get("source_filename", "unknown")
        idx = per_file_counter[filename]
        node.id_ = hashlib.md5(f"{filename}:{idx}".encode()).hexdigest()
        per_file_counter[filename] += 1
    return nodes


def build_index(documents: list, chroma_path: str):
    """Split documents into nodes, assign stable IDs, embed, and upsert into ChromaDB."""
    embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

    chroma_client = chromadb.PersistentClient(path=chroma_path)
    collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)

    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Split first so we can assign stable IDs before any embedding occurs
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
    nodes = assign_stable_ids(nodes)

    # from_nodes embeds and upserts; ChromaDB uses node.id_ as the document key
    VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True,
    )
    return collection


def main() -> None:
    args = parse_args()

    print(f"[ingest] docs-dir   : {Path(args.docs_dir).resolve()}")
    print(f"[ingest] chroma-path: {Path(args.chroma_path).resolve()}")
    print(f"[ingest] embedding  : {EMBEDDING_MODEL}")
    print(f"[ingest] collection : {CHROMA_COLLECTION}")
    print()

    documents, article_count = load_documents(args.docs_dir)
    collection = build_index(documents, args.chroma_path)

    chunk_count = collection.count()
    print()
    print(f"✓ {article_count} article(s) processed, {chunk_count} chunk(s) stored in ChromaDB")


if __name__ == "__main__":
    main()
