"""
Farming Agent — LangChain Agent with tools for agricultural queries
"""
import logging
from typing import Optional

from rag.pipeline import run_rag_pipeline
from modules.weather import get_weather_summary
from modules.market import get_market_prices
from modules.crops import get_crop_recommendation
from modules.pest import diagnose_pest
from modules.irrigation import get_irrigation_advice
from modules.fertilizer import get_fertilizer_advice
from modules.schemes import get_relevant_schemes

logger = logging.getLogger(__name__)

# Query intent keywords
INTENT_MAP = {
    "weather":    ["weather", "rain", "temperature", "humidity", "forecast", "climate", "storm", "drought"],
    "crop":       ["crop", "plant", "grow", "sow", "harvest", "variety", "seed", "cultivation", "kharif", "rabi"],
    "pest":       ["pest", "disease", "insect", "fungus", "yellow", "spot", "wilt", "virus", "blight", "rot", "spray"],
    "irrigation": ["water", "irrigation", "drip", "sprinkler", "moisture", "drought", "flood"],
    "fertilizer": ["fertilizer", "npk", "urea", "manure", "compost", "nutrient", "soil health", "organic"],
    "market":     ["price", "mandi", "market", "sell", "rate", "onion", "tomato", "wheat", "rice"],
    "schemes":    ["scheme", "subsidy", "insurance", "loan", "pm-kisan", "pmfby", "kcc", "government", "benefit"],
}


def detect_intent(query: str) -> str:
    """Detect primary intent from query keywords."""
    query_lower = query.lower()
    for intent, keywords in INTENT_MAP.items():
        if any(kw in query_lower for kw in keywords):
            return intent
    return "general"


async def process_farming_query(
    query: str,
    language: str = "English",
    location: Optional[str] = None,
    state: Optional[str] = None,
    crop: Optional[str] = None,
    soil_type: Optional[str] = None,
    season: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> dict:
    """
    Main entry point for the farming agent.
    Routes queries to the appropriate module then enhances with RAG + Granite.
    """
    intent = detect_intent(query)
    logger.info(f"Query intent: {intent} | query='{query[:60]}'")

    # Enrich query with context
    context_parts = []
    if location:
        context_parts.append(f"Location: {location}")
    if state:
        context_parts.append(f"State: {state}")
    if crop:
        context_parts.append(f"Crop: {crop}")
    if soil_type:
        context_parts.append(f"Soil type: {soil_type}")
    if season:
        context_parts.append(f"Season: {season}")

    enriched_query = query
    if context_parts:
        enriched_query = f"{query} [Context: {', '.join(context_parts)}]"

    # Gather live data based on intent
    live_data: dict = {}

    if intent == "weather" and (lat and lon):
        try:
            live_data["weather"] = await get_weather_summary(lat, lon)
        except Exception as e:
            logger.warning(f"Weather fetch failed: {e}")

    if intent == "market":
        try:
            live_data["market"] = await get_market_prices(crop or "wheat", state)
        except Exception as e:
            logger.warning(f"Market fetch failed: {e}")

    # Run RAG pipeline for knowledge-backed response
    rag_result = run_rag_pipeline(
        query=enriched_query,
        language=language,
        category_filter=intent if intent != "general" else None,
    )

    # Merge live data into response
    if live_data:
        live_summary = _format_live_data(live_data, intent)
        rag_result["answer"] = live_summary + "\n\n" + rag_result["answer"]
        rag_result["live_data"] = live_data

    rag_result["intent"] = intent
    return rag_result


def _format_live_data(live_data: dict, intent: str) -> str:
    """Format live API data into a brief section."""
    lines = ["**📡 Live Data**"]

    if "weather" in live_data:
        w = live_data["weather"]
        lines.append(
            f"🌡 Temperature: {w.get('temperature_2m', 'N/A')}°C | "
            f"💧 Humidity: {w.get('relative_humidity_2m', 'N/A')}% | "
            f"🌧 Precipitation: {w.get('precipitation', 'N/A')} mm"
        )

    if "market" in live_data:
        prices = live_data["market"]
        if prices:
            lines.append("💰 Current Mandi Prices:")
            for entry in prices[:3]:
                lines.append(f"  • {entry.get('commodity', '')}: ₹{entry.get('modal_price', 'N/A')}/quintal @ {entry.get('market', '')}")

    return "\n".join(lines)
