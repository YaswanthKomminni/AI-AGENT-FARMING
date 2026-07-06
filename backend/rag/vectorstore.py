"""
RAG Pipeline — ChromaDB Vector Store Integration
"""
import logging
from functools import lru_cache
from typing import Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@lru_cache
def get_chroma_client() -> chromadb.PersistentClient:
    client = chromadb.PersistentClient(
        path=settings.chroma_persist_dir,
        settings=ChromaSettings(anonymized_telemetry=False),
    )
    logger.info(f"ChromaDB client initialised at {settings.chroma_persist_dir}")
    return client


def get_vectorstore():
    """Return (or create) the farming knowledge collection."""
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=settings.chroma_collection_name,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def add_documents(texts: list[str], metadatas: list[dict], ids: list[str]) -> None:
    """Add documents to the vector store using sentence-transformers embeddings."""
    from rag.embeddings import get_embedder

    collection = get_vectorstore()
    embedder = get_embedder()
    embeddings = embedder.encode(texts, show_progress_bar=True).tolist()

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    logger.info(f"Upserted {len(texts)} documents into '{settings.chroma_collection_name}'")


def similarity_search(query: str, n_results: int = 5, where: Optional[dict] = None) -> list[dict]:
    """
    Return top-k relevant documents for a query.
    Returns list of {text, metadata, distance}.
    """
    from rag.embeddings import get_embedder

    collection = get_vectorstore()
    embedder = get_embedder()
    query_embedding = embedder.encode([query]).tolist()

    kwargs: dict = {"query_embeddings": query_embedding, "n_results": n_results}
    if where:
        kwargs["where"] = where

    results = collection.query(**kwargs)

    docs = []
    for i, doc in enumerate(results["documents"][0]):
        docs.append({
            "text": doc,
            "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
            "distance": results["distances"][0][i] if results["distances"] else 1.0,
        })
    return docs
