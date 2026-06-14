"""Cosine-similarity helpers for semantic matching between embeddings."""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(vec1, vec2):
    """Return the cosine similarity score for two embedding vectors."""
    return cosine_similarity([vec1], [vec2])[0][0]


def find_best_match(query_vec, candidate_vecs):
    """Return the index and score of the best matching candidate vector."""
    scores = cosine_similarity([query_vec], candidate_vecs)[0]
    best_idx = int(np.argmax(scores))
    return best_idx, float(scores[best_idx])
