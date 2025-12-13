"""
Central configuration for the documentation RAG system.

This file contains all constants that control:
- models
- chunking behavior
- data and index paths

Keeping these values in one place makes the system
easy to tune and reason about.
"""

# =========================
# Embedding model settings
# =========================

# Sentence embedding model used for semantic retrieval.
# Chosen for strong performance on technical text and
# compatibility with cosine similarity.
EMBEDDING_MODEL = "intfloat/e5-base"


# =========================
# Chunking configuration
# =========================

# Maximum number of words per chunk.
# Larger chunks preserve context, smaller chunks improve precision.
CHUNK_SIZE = 500

# NOTE:
# CHUNK_OVERLAP is currently unused.
# It is kept here intentionally to allow easy experimentation
# with overlapping chunks in the future if needed.
CHUNK_OVERLAP = 100


# =========================
# Data paths
# =========================

# Raw documentation files (Markdown).
RAW_DATA_DIR = "data/raw"

# Derived artifacts such as embeddings and FAISS index.
PROCESSED_DATA_DIR = "data/processed"

# Paths to generated artifacts.
INDEX_PATH = f"{PROCESSED_DATA_DIR}/faiss.index"
EMBEDDINGS_PATH = f"{PROCESSED_DATA_DIR}/embeddings.npy"
DOCS_PATH = f"{PROCESSED_DATA_DIR}/docs.pkl"