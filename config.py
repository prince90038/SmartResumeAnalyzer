import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TEMPERATURE = 0

def get_llm():
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME
        )
    return _embedding_model
