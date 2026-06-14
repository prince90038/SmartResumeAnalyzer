"""Shared embedding helper used by the similarity-based matching logic."""

from config import get_embedding_model


def embed_texts(texts):
    """Embed a list of texts into vectors using the configured embedding model."""
    model = get_embedding_model()
    return model.embed_documents(texts)
