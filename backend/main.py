"""
FarmWise AI — FastAPI Application Entry Point
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from rag.vectorstore import get_vectorstore
from routers import chat, weather, market, voice, schemes

settings = get_settings()
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: eagerly warm up ALL slow components so the first user
    request is fast instead of hitting a 16-second cold-start.
    """
    logger.info("FarmWise AI starting up — warming up components...")

    # 1. Pre-load embedding model (16s cold-start — do it now, not on first query)
    try:
        from rag.embeddings import get_embedder
        emb = get_embedder()
        emb.encode(["warmup"])          # force weights into memory
        logger.info("Embedding model ready (all-MiniLM-L6-v2)")
    except Exception as exc:
        logger.warning(f"Embedding warmup warning: {exc}")

    # 2. Pre-load ChromaDB collection
    try:
        col = get_vectorstore()
        logger.info(f"Vector store ready ({col.count()} docs)")
    except Exception as exc:
        logger.warning(f"Vector store init warning: {exc}")

    # 3. Pre-load IBM Granite LLM (creates authenticated client)
    try:
        from agents.granite import get_granite_llm
        get_granite_llm()
        logger.info("IBM Granite LLM client ready")
    except Exception as exc:
        logger.warning(f"Granite LLM warmup warning: {exc}")

    logger.info("FarmWise AI ready to serve requests")
    yield
    logger.info("FarmWise AI shutting down")


app = FastAPI(
    title="FarmWise AI",
    description="Smart Farming Advisor powered by IBM Granite + RAG",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────
app.include_router(chat.router,    prefix="/api/chat",    tags=["Chat"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(market.router,  prefix="/api/market",  tags=["Market"])
app.include_router(voice.router,   prefix="/api/voice",   tags=["Voice"])
app.include_router(schemes.router, prefix="/api/schemes", tags=["Schemes"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "FarmWise AI", "version": "1.0.0"}
