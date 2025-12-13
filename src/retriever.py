import pickle
from typing import List, Dict

import faiss
import numpy as np

from src.config import INDEX_PATH, DOCS_PATH


def load_faiss_index():
    """
    Load the FAISS index and associated document metadata from disk.

    This is kept separate from retrieval logic so that index loading
    can be reasoned about and debugged independently.
    """
    index = faiss.read_index(INDEX_PATH)

    with open(DOCS_PATH, "rb") as f:
        documents = pickle.load(f)

    return index, documents


def retrieve_documents(
    query_embedding: np.ndarray,
    top_k: int = 3
) -> List[Dict[str, str]]:
    """
    Retrieve the top-k most relevant documentation chunks for a query.

    Assumptions:
    - query_embedding is already normalized
    - the FAISS index was built using normalized embeddings
      (so inner product corresponds to cosine similarity)

    Returns:
    - a list of document chunks with text and source metadata
    """
    index, documents = load_faiss_index()

    # FAISS expects shape (num_queries, embedding_dim)
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)

    scores, indices = index.search(query_embedding, top_k)

    results: List[Dict[str, str]] = []
    for doc_index in indices[0]:
        results.append(documents[doc_index])

    return results