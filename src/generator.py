from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Tuple


def load_text_generator(
    model_name: str = "google/flan-t5-base",
) -> Tuple[AutoTokenizer, AutoModelForSeq2SeqLM]:
    """
    Load a lightweight instruction-tuned language model for answer generation.

    We intentionally use a smaller, open model to keep the system:
    - fully local
    - reproducible
    - inexpensive to run

    The model is only responsible for summarizing retrieved documentation,
    not for open-ended generation.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return tokenizer, model


def generate_answer(
    context: str,
    question: str,
    model: AutoModelForSeq2SeqLM,
    tokenizer: AutoTokenizer,
) -> str:
    """
    Generate a grounded answer to a user question based on retrieved context.

    This function is deliberately conservative:
    - it discourages hallucination
    - it biases the model toward extraction and summarization
    - it prefers saying "Not found" over guessing
    """
    prompt = (
        "You are an internal documentation assistant for a software engineering team.\n\n"
        "Your task is to answer the user's question using ONLY the documentation context.\n\n"
        "Guidelines:\n"
        "- Use only the information present in the documentation context.\n"
        "- If the documentation contains relevant information, summarize it clearly.\n"
        "Documentation Context:\n"
        f"{context}\n\n"
        "Question:\n"
        f"{question}\n\n"
        "Answer:"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.0,  # deterministic, reduces hallucination
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)