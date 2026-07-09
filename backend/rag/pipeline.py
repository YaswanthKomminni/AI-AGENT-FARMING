"""
RAG Pipeline — Retrieval + IBM Granite Generation
Optimised: response cache, retry on 429, reduced token count, faster retrieval.
"""
import logging
import time
import hashlib
from typing import Optional
from functools import lru_cache

from rag.vectorstore import similarity_search
from agents.granite import get_granite_llm

logger = logging.getLogger(__name__)

# ── Simple in-memory response cache (query hash → answer) ────────────────────
_response_cache: dict[str, dict] = {}
CACHE_MAX = 200          # max entries to keep


def _cache_key(query: str, language: str, category: Optional[str]) -> str:
    raw = f"{query.strip().lower()}|{language}|{category}"
    return hashlib.md5(raw.encode()).hexdigest()


# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are FarmWise AI, a strictly focused agricultural AI assistant for Indian farmers. "
    "You are ONLY allowed to answer questions directly related to farming (crops, pests, soil, irrigation, fertilizer, livestock), weather/temperature, mandi/market prices, and government schemes/subsidies. "
    "CRITICAL behavioral rule: If the user's question is NOT about farming, weather, temperature, mandi prices, or government schemes, you must NOT answer the question. Under no circumstances should you provide general information, write code, tell jokes, solve math, or answer other general knowledge queries. "
    "Instead, you must reply EXACTLY with: 'I can only help with questions related to farming, weather/temperature, market prices, and government schemes. Please ask a question related to these topics.' "
    "Do not provide any other information or explanation for off-topic questions."
)


def build_rag_prompt(query: str, context_docs: list[dict], language: str = "English") -> str:
    """Build formatted string prompt for WatsonxLLM using Granite template."""
    context_parts = []
    for i, doc in enumerate(context_docs, 1):
        source = doc.get("metadata", {}).get("source", "Knowledge Base")
        context_parts.append(f"[Source {i}: {source}]\n{doc['text']}")

    context_str = "\n\n".join(context_parts) if context_parts else "Use your general agricultural knowledge."
    lang_instruction = f"\n\nPlease answer in {language}." if language != "English" else ""

    user_content = (
        f"Relevant farming knowledge:\n{context_str}\n\n"
        f"Farmer's question: {query}{lang_instruction}"
    )
    
    prompt = (
        f"<|system|>\n{SYSTEM_PROMPT}<|end|>\n"
        f"<|user|>\n{user_content}<|end|>\n"
        f"<|assistant|>\n"
    )
    return prompt


def _invoke_with_retry(llm, prompt: str, max_retries: int = 3) -> str:
    """
    Invoke the LLM with exponential back-off retry on rate-limit (429) errors.
    IBM Cloud Lite plan has a 10 concurrent-request limit.
    """
    delay = 3  # seconds
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            if hasattr(response, "content"):
                return response.content
            return str(response)
        except Exception as e:
            err_str = str(e).lower()
            is_rate_limit = "429" in str(e) or "consumption_limit" in err_str or "rate" in err_str
            if is_rate_limit and attempt < max_retries - 1:
                wait = delay * (2 ** attempt)   # 3s, 6s, 12s
                logger.warning(f"IBM Granite rate-limited (429). Retry {attempt+1}/{max_retries} in {wait}s...")
                time.sleep(wait)
                continue
            # Non-retryable or exhausted retries
            raise


def run_rag_pipeline(
    query: str,
    language: str = "English",
    category_filter: Optional[str] = None,
    n_docs: int = 3,          # reduced from 5 → 3 for speed
) -> dict:
    """
    Full RAG pipeline:
    1. Check cache
    2. Retrieve relevant documents from ChromaDB
    3. Build chat messages with context
    4. Generate response with IBM Granite (with retry)
    5. Cache + return response + sources
    """
    # Step 1: Cache check
    key = _cache_key(query, language, category_filter)
    if key in _response_cache:
        logger.info(f"Cache hit for query: '{query[:40]}'")
        cached = _response_cache[key].copy()
        cached["cached"] = True
        return cached

    # Step 2: Retrieve (top-3 docs only for speed)
    where_filter = None
    if category_filter:
        where_filter = {"category": {"$eq": category_filter}}

    try:
        docs = similarity_search(query, n_results=n_docs, where=where_filter)
        logger.info(f"Retrieved {len(docs)} docs for: '{query[:40]}'")
    except Exception as e:
        logger.warning(f"Retrieval failed: {e}. Continuing without context.")
        docs = []

    # Step 3: Build formatted prompt string
    prompt = build_rag_prompt(query, docs, language)

    # Step 4: Generate with IBM Granite (retry on 429)
    try:
        llm = get_granite_llm()
        response_text = _invoke_with_retry(llm, prompt)
    except Exception as e:
        logger.error(f"LLM generation failed after retries: {e}", exc_info=True)
        # Fall back to mock response so the app stays usable
        from agents.granite import _MockGraniteLLM
        response_text = _MockGraniteLLM().invoke(query)

    # Step 5: Extract sources
    sources = []
    for doc in docs:
        src = doc.get("metadata", {}).get("source", "")
        if src and src not in sources:
            sources.append(src)

    result = {
        "answer": response_text,
        "sources": sources,
        "retrieved_docs": len(docs),
        "language": language,
        "cached": False,
    }

    # Store in cache (evict oldest if full)
    if len(_response_cache) >= CACHE_MAX:
        oldest = next(iter(_response_cache))
        del _response_cache[oldest]
    _response_cache[key] = result

    return result
