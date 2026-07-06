"""
Embedding Model — sentence-transformers wrapper
"""
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from config import get_settings

settings = get_settings()


@lru_cache
def get_embedder() -> SentenceTransformer:
    model = SentenceTransformer(settings.embedding_model)
    return model
