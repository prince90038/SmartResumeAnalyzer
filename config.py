"""Application-level configuration for LLM and embedding helpers."""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"
TEMPERATURE = 0

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_llm = None
_embedding_model = None


def get_llm():
    """Return the cached Gemini chat model used by the pipeline."""
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
    return _llm


def get_embedding_model():
    """Return the cached embedding model used for semantic matching."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
        )
    return _embedding_model
