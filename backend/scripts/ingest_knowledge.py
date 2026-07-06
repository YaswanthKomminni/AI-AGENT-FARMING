"""
Knowledge Ingestion Script
Reads all .txt files from knowledge_base/ and loads them into ChromaDB.
Run once before starting the server: python scripts/ingest_knowledge.py
"""
import sys
import os
import uuid
import re

# Allow imports from backend/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from rag.vectorstore import add_documents, get_chroma_client
from config import get_settings

settings = get_settings()

KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")

CATEGORY_MAP = {
    "crops.txt":             "crop",
    "pest_diseases.txt":     "pest",
    "fertilizers.txt":       "fertilizer",
    "irrigation.txt":        "irrigation",
    "government_schemes.txt":"schemes",
    "farming_practices.txt": "general",
}


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks at sentence boundaries."""
    sentences = re.split(r"(?<=[.!?])\s+|\n{2,}", text)
    chunks = []
    current = []
    current_len = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if current_len + len(sentence) > chunk_size and current:
            chunks.append(" ".join(current))
            # Overlap: keep last few sentences
            while current and current_len > overlap:
                removed = current.pop(0)
                current_len -= len(removed)
        current.append(sentence)
        current_len += len(sentence)

    if current:
        chunks.append(" ".join(current))

    return [c for c in chunks if len(c.strip()) > 50]


def ingest_all():
    logger.info("🌾 Starting FarmWise AI knowledge base ingestion …")

    if not os.path.isdir(KNOWLEDGE_DIR):
        logger.error(f"Knowledge directory not found: {KNOWLEDGE_DIR}")
        sys.exit(1)

    total_docs = 0

    for filename in os.listdir(KNOWLEDGE_DIR):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(KNOWLEDGE_DIR, filename)
        category = CATEGORY_MAP.get(filename, "general")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunk_text(content)
        logger.info(f"  📄 {filename} → {len(chunks)} chunks (category={category})")

        texts = []
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            doc_id = f"{filename}_{i}"
            texts.append(chunk)
            metadatas.append({
                "source": filename.replace(".txt", "").replace("_", " ").title(),
                "category": category,
                "chunk_index": i,
                "filename": filename,
            })
            ids.append(doc_id)

        add_documents(texts=texts, metadatas=metadatas, ids=ids)
        total_docs += len(chunks)

    logger.success(f"✅ Ingestion complete. Total chunks loaded: {total_docs}")

    # Verify
    client = get_chroma_client()
    collection = client.get_collection(settings.chroma_collection_name)
    logger.info(f"📦 ChromaDB collection '{settings.chroma_collection_name}': {collection.count()} documents")


if __name__ == "__main__":
    ingest_all()
