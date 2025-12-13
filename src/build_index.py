import os
import pickle
from typing import List, Dict

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.ingest import ingest_raw_documents
from src.config import (
    EMBEDDING_MODEL,
    PROCESSED_DATA_DIR,
    EMBEDDINGS_PATH,
    DOCS_PATH,
    INDEX_PATH,
)


def build_index():
    """
    Build the vector index for the documentation RAG system.

    This script performs an offline indexing step:
    - ingest and chunk markdown documentation
    - compute sentence embeddings
    - store embeddings and metadata
    - build and persist a FAISS index for retrieval

    It is intentionally run as a standalone step so that
    indexing does not happen at query time.
    """
    print("Loading and processing documentation...")
    documents: List[Dict[str, str]] = ingest_raw_documents()

    if not documents:
        raise RuntimeError(
            "No documentation found. "
            "Please ensure Markdown files exist under data/raw."
        )

    print(f"Processed {len(documents)} documentation chunks")

    # Extract raw text for embedding generation
    texts = [doc["text"] for doc in documents]

    print("Initializing embedding model...")
    embedder = SentenceTransformer(EMBEDDING_MODEL)

    print("Generating embeddings...")
    embeddings = embedder.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    # Ensure output directory exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    print("Persisting embeddings and document metadata...")
    np.save(EMBEDDINGS_PATH, embeddings)

    with open(DOCS_PATH, "wb") as f:
        pickle.dump(documents, f)

    print("Building FAISS vector index...")
    embedding_dim = embeddings.shape[1]

    # Using inner product on normalized vectors gives cosine similarity
    index = faiss.IndexFlatIP(embedding_dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    print("Indexing complete.")


if __name__ == "__main__":
    build_index()