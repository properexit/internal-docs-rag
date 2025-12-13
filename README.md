# Internal Documentation Assistant (RAG)

A domain-specific Retrieval-Augmented Generation (RAG) system for answering
questions over internal software documentation using FastAPI documents.

The system retrieves relevant Markdown documentation using semantic search
and generates grounded answers strictly from the retrieved content.
It is designed as an internal engineering tool with a strong focus on
correctness, explainability, and hallucination control.

---

## ✨ Key Features

- Semantic retrieval over Markdown documentation using FAISS
- Conservative answer generation with strict grounding
- Source attribution for every answer
- Modular ingestion, retrieval, and generation pipeline
- Fully local and reproducible (no paid APIs)

---

## 🏗️ Architecture Overview

             ┌─────────────────────┐
             │  Markdown Docs (.md)│
             │     data/raw/       │
             └──────────┬──────────┘
                        │
                        ▼
          ┌────────────────────┐
          │  Ingestion Pipeline│
          │  - clean markdown  │
          │  - chunk by section│
          └──────────┬─────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │  Embedding Generation   │
            │  SentenceTransformer    │
            │  (intfloat/e5-base)     │
            └──────────┬──────────────┘
                       │
                       ▼
      ┌─────────────────────────────────┐
      │  Vector Index (FAISS)           │
      │  - cosine similarity search     │
      │  - embeddings + metadata        │
      └──────────┬──────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │  Query-Time Pipeline                │
    │  - embed user question              │
    │  - retrieve top-k relevant chunks   │
    │  - select most relevant context     │
    └──────────┬──────────────────────────┘
               │
               ▼
 ┌──────────────────────────────────────────┐
 │  Answer Generation (FLAN-T5)             │
 │  - grounded summarization                │
 │  - deterministic decoding                │
 │  - refusal if info not present           │
 └──────────┬──────────────────────────────┘
            │
            ▼
    ┌─────────────────────────┐
    │  Streamlit UI           │
    │  - answer               │
    │  - sources              │
    │  - debug context view   │
    └─────────────────────────┘

---

## 🧪 Example Queries

### Authentication

**Question**

Which authentication method is mentioned?

**Answer**

OAuth2 with Password (and hashing), Bearer with JWT tokens.

**Sources**
- authentication.md
- dependency_injection.md

---

### Presence Query

**Question**

Is OAuth2 mentioned in the documentation?

**Answer**

Yes.

**Sources**
- authentication.md


---

## 🚀 How to Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.build_index
streamlit run app/ui.py


⸻

🎯 Design Philosophy
	•	Retrieval first, generation second
	•	Prefer extraction over abstraction
	•	Fail explicitly instead of hallucinating
	•	Keep the system explainable and debuggable
	•	Optimize for correctness over creativity

⸻

📄 License

MIT

---
