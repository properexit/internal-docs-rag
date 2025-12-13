# Internal Documentation Assistant (RAG)

A domain-specific Retrieval-Augmented Generation (RAG) system for answering
questions over internal software documentation.

The system retrieves relevant Markdown documentation using semantic search
and generates grounded answers strictly from the retrieved content.
It is designed as an internal engineering tool with a strong focus on
correctness, explainability, and hallucination control.

---

## ✨ Key Features

- Semantic retrieval over Markdown documentation using FAISS
- Conservative answer generation with strict grounding
- Explicit refusal when information is not present in the documentation
- Source attribution for every answer
- Modular ingestion, retrieval, and generation pipeline
- Fully local and reproducible (no paid APIs)

---

## 🏗️ Architecture Overview

             ┌─────────────────────┐
             │  Markdown Docs (.md) │
             │     data/raw/        │
             └──────────┬──────────┘
                        │
                        ▼
          ┌────────────────────┐
          │  Ingestion Pipeline │
          │  - clean markdown   │
          │  - chunk by section │
          └──────────┬─────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │  Embedding Generation    │
            │  SentenceTransformer     │
            │  (intfloat/e5-base)      │
            └──────────┬──────────────┘
                       │
                       ▼
      ┌─────────────────────────────────┐
      │  Vector Index (FAISS)            │
      │  - cosine similarity search      │
      │  - embeddings + metadata         │
      └──────────┬──────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │  Query-Time Pipeline                 │
    │  - embed user question               │
    │  - retrieve top-k relevant chunks    │
    │  - select most relevant context      │
    └──────────┬──────────────────────────┘
               │
               ▼
 ┌──────────────────────────────────────────┐
 │  Answer Generation (FLAN-T5)              │
 │  - grounded summarization                 │
 │  - deterministic decoding                │
 │  - refusal if info not present            │
 └──────────┬──────────────────────────────┘
            │
            ▼
    ┌─────────────────────────┐
    │  Streamlit UI            │
    │  - answer                │
    │  - sources               │
    │  - debug context view    │
    └─────────────────────────┘

---

## 🧪 Example Queries

### Authentication
**Which authentication method is mentioned?**
**OAuth2 with Password (and hashing), Bearer with JWT tokens.r**
**authentication.md**
**dependency_injection.md**
**# OAuth2 with Password (and hashing), Bearer with JWT tokens[¶](#oauth2-with-password-and-hashing-bearer-with-jwt-tokens "Permanent link"){. preview=""} Now that we have all the security flow, let\'s make the application actually secure, using [JWT]{.abbr title="JSON Web Tokens"} tokens and secure password hashing. This code is something you can actually use in your application, save the password hashes in your database, etc. We are going to start from where we left in the previous chapter and increment it.**

---

## 🚀 How to Run

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.build_index
streamlit run app/ui.py