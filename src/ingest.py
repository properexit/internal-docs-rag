import os
import re
from typing import List, Dict

from src.config import RAW_DATA_DIR, CHUNK_SIZE


def read_markdown_file(file_path: str) -> str:
    """
    Read a Markdown file from disk and return its raw text.

    We keep this function minimal on purpose: parsing and cleaning
    are handled separately to keep responsibilities clear.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def clean_markdown_text(text: str) -> str:
    """
    Clean Markdown text before chunking.

    The goal here is NOT heavy preprocessing.
    We only remove artifacts introduced during HTML → Markdown
    conversion that confuse embedding models.
    """
    # Remove Pandoc-style header anchors: {#section-name}
    text = re.sub(r"\{#.*?\}", "", text)

    # Remove leftover 'headerlink' artifacts from HTML conversions
    text = re.sub(r"headerlink", "", text, flags=re.IGNORECASE)

    # Normalize excessive whitespace while preserving structure
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
    """
    Split documentation text into semantically meaningful chunks.

    Strategy:
    1. Split by Markdown section headers (##, ###, etc.)
    2. Further split long sections into fixed-size chunks

    This preserves topic coherence while keeping chunks
    small enough for precise retrieval.
    """
    chunks: List[str] = []

    # Split on second-level (and deeper) markdown headers
    sections = re.split(r"\n##+\s", text)

    for section in sections:
        words = section.split()

        for start in range(0, len(words), chunk_size):
            chunk = " ".join(words[start:start + chunk_size])

            # Skip very small or empty chunks
            if len(chunk.strip()) > 50:
                chunks.append(chunk)

    return chunks


def ingest_raw_documents() -> List[Dict[str, str]]:
    """
    Ingest all Markdown documentation under the raw data directory.

    For each document, we:
    - read the file
    - clean conversion artifacts
    - split into semantic chunks
    - attach source metadata

    The returned structure is intentionally simple and explicit
    to make downstream debugging and citation straightforward.
    """
    documents: List[Dict[str, str]] = []

    for root, _, files in os.walk(RAW_DATA_DIR):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            file_path = os.path.join(root, filename)

            raw_text = read_markdown_file(file_path)
            cleaned_text = clean_markdown_text(raw_text)
            chunks = split_into_chunks(cleaned_text)

            relative_source = os.path.relpath(file_path, RAW_DATA_DIR)

            for chunk in chunks:
                documents.append(
                    {
                        "text": chunk,
                        "source": relative_source,
                    }
                )

    return documents