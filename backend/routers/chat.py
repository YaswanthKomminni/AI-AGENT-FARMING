"""
API Router: Chat — Main conversational endpoint
"""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.farming_agent import process_farming_query
from translation.translator import translate_text, get_supported_languages

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    language: str = "English"
    location: Optional[str] = None
    state: Optional[str] = None
    crop: Optional[str] = None
    soil_type: Optional[str] = None
    season: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    translate_input: bool = False


class ChatResponse(BaseModel):
    answer: str
    intent: str
    sources: list[str]
    retrieved_docs: int
    language: str
    live_data: Optional[dict] = None


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint — runs the full RAG + IBM Granite pipeline.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Translate input to English for processing if needed
    query = request.message
    if request.translate_input and request.language != "English":
        query = translate_text(request.message, target_language="English", source_language="auto")

    try:
        result = await process_farming_query(
            query=query,
            language=request.language,
            location=request.location,
            state=request.state,
            crop=request.crop,
            soil_type=request.soil_type,
            season=request.season,
            lat=request.lat,
            lon=request.lon,
        )

        # Translate response back to user language if not English
        answer = result["answer"]
        if request.language != "English":
            try:
                answer = translate_text(answer, target_language=request.language)
            except Exception as e:
                logger.warning(f"Response translation failed: {e}")

        return ChatResponse(
            answer=answer,
            intent=result.get("intent", "general"),
            sources=result.get("sources", []),
            retrieved_docs=result.get("retrieved_docs", 0),
            language=request.language,
            live_data=result.get("live_data"),
        )

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/languages")
async def list_languages():
    """List supported languages."""
    return get_supported_languages()


@router.get("/examples")
async def example_queries():
    """Return example farming queries."""
    return {
        "examples": [
            "What crop should I grow this season in black soil?",
            "My tomato leaves have yellow spots. What should I do?",
            "What fertilizer should I use for paddy?",
            "How much water does cotton require this week?",
            "What is today's mandi price for onions?",
            "Which government schemes am I eligible for?",
            "Will it rain tomorrow in Pune?",
            "Is there any pest outbreak for rice crops?",
            "What are organic alternatives to urea for wheat?",
            "When should I irrigate my wheat crop?",
        ]
    }
