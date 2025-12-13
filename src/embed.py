import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

from src.config import EMBEDDING_MODEL, EMBEDDINGS_PATH, DOCS_PATH

def embed_documents(docs):
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(docs, show_progress_bar=True)
    return embeddings

def save_embeddings(embeddings, docs):
    np.save(EMBEDDINGS_PATH, embeddings)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)