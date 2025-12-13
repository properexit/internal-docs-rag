def recall_at_k(retrieved_indices, relevant_indices, k=5):
    return len(set(retrieved_indices[:k]) & set(relevant_indices)) > 0

def evaluate_retrieval(index, embeddings, ground_truth):
    # ground_truth: {query_id: relevant_doc_id}
    # Fill with your evaluation logic
    pass