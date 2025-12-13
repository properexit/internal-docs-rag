import os
import sys
from typing import Tuple, List, Dict

import streamlit as st
from sentence_transformers import SentenceTransformer

# -------------------------------------------------------------------
# Project path setup
# -------------------------------------------------------------------
# This allows running the Streamlit app from the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.retriever import retrieve_documents
from src.generator import load_text_generator, generate_answer


# -------------------------------------------------------------------
# Model loading (cached for Streamlit)
# -------------------------------------------------------------------
@st.cache_resource
def load_models() -> Tuple[SentenceTransformer, object, object]:
    """
    Load all models once and cache them for the Streamlit session.

    - SentenceTransformer: used for retrieval embeddings
    - Text generator: used for grounded answer generation
    """
    embedder = SentenceTransformer("intfloat/e5-base")
    tokenizer, generator_model = load_text_generator()
    return embedder, tokenizer, generator_model


embedder, tokenizer, generator_model = load_models()


# -------------------------------------------------------------------
# UI layout
# -------------------------------------------------------------------
st.title("Internal Documentation Assistant")
st.caption(
    "Ask questions about API usage, configuration, or system behavior. "
    "Answers are generated strictly from the provided documentation."
)

question = st.text_input(
    "Ask a question",
    placeholder="e.g. Which authentication mechanism is mentioned?"
)


# -------------------------------------------------------------------
# Query handling
# -------------------------------------------------------------------
if question:
    # Encode the query for semantic retrieval
    query_embedding = embedder.encode([question])

    # Retrieve relevant documentation chunks
    retrieved_docs: List[Dict[str, str]] = retrieve_documents(
        query_embedding,
        top_k=3,
    )

    # Use only the most relevant chunk for answer generation
    # This reduces noise and improves precision for factual questions
    context = retrieved_docs[0]["text"] if retrieved_docs else ""

    # Generate grounded answer
    answer = generate_answer(
        context=context,
        question=question,
        model=generator_model,
        tokenizer=tokenizer,
    )

    # ----------------------------------------------------------------
    # Display results
    # ----------------------------------------------------------------
    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")
    sources = sorted({doc["source"] for doc in retrieved_docs})
    for source in sources:
        st.write(f"- {source}")

    # Optional debug view (useful during development)
    with st.expander("Debug: Context passed to the language model"):
        st.text(context[:2000])