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


from translation.translator import translate_text

def is_query_on_topic(query: str) -> bool:
    """Check if the query is related to farming, weather/temperature, market prices, or schemes."""
    import re
    # Normalize query: lowercase and remove punctuation
    query_clean = re.sub(r'[^\w\s-]', ' ', query.lower())
    words = query_clean.split()

    if not words:
        return False

    # 1. Blacklist check (programming, entertainment, off-topic fields)
    blacklist_keywords = {
        "python", "javascript", "java", "script", "code", "programming", "develop", "software", "html", "css", "database", "sql", 
        "movie", "song", "poem", "joke", "cricket", "football", "soccer", "actor", "actress", "director", "sing", "dance", "politics", "election"
    }
    if any(w in blacklist_keywords for w in words):
        return False

    # 2. Allow greetings and bot-specific meta questions
    meta_keywords = {
        "hi", "hello", "hey", "hola", "namaste", "pranam", "pranama", "greetings", "morning", "evening", "afternoon",
        "who", "what", "how", "you", "assistant", "farmwise", "help", "capabilities", "purpose", "info",
        "are", "is", "your", "can", "do", "name", "about", "describe", "yourself", "introduce", "me", "to", "the", 
        "bot", "ai", "smart", "tell", "show", "details", "work", "greeting", "exist", "created",
        "thank", "thanks", "great", "nice", "good", "bye", "goodbye", "care", "welcome", "awesome", "cool",
        "that", "this", "it", "well", "fine", "so", "very", "much", "day", "meet", "doing", "going", "up",
        "am", "i", "a", "an", "ok", "okay", "glad", "happy", "talk", "chat", "speak", "please", "with",
        "take", "later", "soon", "again"
    }
    # If it's a short message containing only meta keywords, it's allowed
    if len(words) <= 5 and all(w in meta_keywords for w in words):
        return True

    # 3. Comprehensive farming-specific and generic topic stems
    farming_specific_stems = [
        # General Agriculture, Farming, Crops, Soil, Fertilizer
        "farm", "agricultur", "cultivat", "agronomy", "horticultur", "floricultur", "field", "land", "soil", "clay", "sand", "silt", "loam", "peat", "chalky", "humus", "fertility", "yield", "crop", "plant", "seed", "sow", "sowing", "harvest", "plow", "plough", "till", "tillage", "tractor", "harvester", "combine", "rotavator", "machinery", "equipment", "greenhouse", "polyhouse", "hydroponic", "aeroponic", "aquaponic", "mulch", "compost", "manure", "organic", "vermicompost", "biofertilizer", "fertilizer", "urea", "npk", "dap", "potash", "phosphate", "nitrogen", "phosphorus", "potassium", "nutrient", "soil health", "soil test", "manure", "cow dung", "zinc", "sulfur", "boron", "iron",
        # Crops & Plants
        "wheat", "rice", "paddy", "cotton", "maize", "corn", "soy", "soybean", "mustard", "tomato", "onion", "potato", "sugarcane", "pulse", "lentil", "gram", "pea", "bean", "millet", "sorghum", "ragi", "bajra", "jute", "rubber", "tea", "coffee", "cardamom", "turmeric", "garlic", "ginger", "chili", "chilli", "pepper", "coconut", "arecanut", "cashew", "mango", "banana", "grape", "citrus", "apple", "guava", "papaya", "pomegranate", "groundnut", "sunflower", "sesame", "castor", "linseed", "safflower", "barley", "oat", "rye", "tobacco", "spice", "coriander", "cumin", "fennel", "fenugreek", "vegetable", "fruit", "flower", "rose", "marigold", "jasmine", "hybrid", "graft", "nursery",
        # Pests, Diseases, Protection
        "pest", "disease", "insect", "bug", "worm", "caterpillar", "aphid", "thrip", "whitefly", "mite", "locust", "borer", "weevil", "fungus", "fungal", "bacteria", "viral", "virus", "nematode", "blight", "wilt", "rot", "mildew", "rust", "spot", "yellowing", "canker", "dieback", "damping off", "weed", "herbicide", "weedicide", "pesticide", "insecticide", "fungicide", "biopesticide", "neem oil", "spray", "dosage", "infestation", "outbreak",
        # Irrigation / Weather specific (always on-topic)
        "irrigation", "drip", "sprinkler", "canal", "well", "borewell", "pump", "watering", "moisture", "drought", "flood", "monsoon", "evaporation", "transpiration", "aquifer", "rainwater", "water harvesting",
        "weather", "forecast", "climate", "humidity", "storm", "frost", "hail", "precipitation", "rain", "today", "tomorrow",
        # Mandi/Market specific
        "mandi", "msp", "apmc", "e-nam",
        # Schemes specific
        "pm-kisan", "pmfby", "kcc", "yojana", "yojan", "pm-kmy", "pmsym", "krishi", "kisan", "fpo", "nabard", "cooperative",
        # Livestock & Allied
        "cow", "cattle", "buffalo", "goat", "sheep", "poultry", "chicken", "hen", "egg", "dairy", "milk", "livestock", "fodder", "feed", "silage", "veterinary", "animal", "bee", "beekeeping", "apiculture", "fish", "fishery", "aquaculture", "sericulture", "silk", "mushroom",
        # Romanized regional terms (Hinglish/regional keywords)
        "kheti", "fasal", "khet", "mitti", "beej", "buwai", "katai", "aloo", "tamatar", "pyaz", "dhan", "chawal", "gehun", "kapas", "ganna", "sarso",
        "paani", "jal", "barish", "barsat", "mausam", "tapman", "sardi", "garmi",
        "bhav", "mandi", "bazaar", "bazar", "karza", "karj", "bima", "beema", "sarkari",
        "khad", "gobar", "keeda", "bimari", "rog", "dawa", "dawae", "keetnashak"
    ]

    generic_stems = [
        "price", "cost", "rate", "sell", "sale", "buy", "wholesale", "retail", "rupee", "inr", "rs", "profit", "loss", "revenue", "income", "trading", "commodity", "value", "paisa", "rupeya", "dam", "daam", "kimat", "keemat",
        "scheme", "subsidy", "subsidies", "insurance", "loan", "credit", "government", "credit card", "bank", "eligible", "eligibility", "benefit", "grant", "support", "financial aid",
        "water", "temperature", "temp", "degree", "celsius", "fahrenheit", "heat", "cold", "wind", "cloud", "sun"
    ]

    has_farming_specific = False

    for word in words:
        # Check farming specific stems
        for stem in farming_specific_stems:
            if len(stem) <= 3:
                if word == stem:
                    has_farming_specific = True
                    break
            else:
                if word.startswith(stem):
                    has_farming_specific = True
                    break
        
        if has_farming_specific:
            return True

        # Check generic stems
        for stem in generic_stems:
            if len(stem) <= 3:
                if word == stem:
                    # just verify if we match any generic word
                    break
            else:
                if word.startswith(stem):
                    # just verify if we match any generic word
                    break

    return False


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
    soil_ph: Optional[float] = None,
    npk_nitrogen: Optional[int] = None,
    npk_phosphorus: Optional[int] = None,
    npk_potassium: Optional[int] = None,
    farm_size: Optional[float] = None,
    irrigation: Optional[str] = None,
) -> dict:
    """
    Main entry point for the farming agent.
    Routes queries to the appropriate module then enhances with RAG + Granite.
    """
    # Translate query to English for topic validation if it's not English
    query_en = query
    try:
        query_en = translate_text(query, target_language="English", source_language="auto")
    except Exception as e:
        logger.warning(f"Could not translate query for topic validation: {e}")

    # Check if query is on topic
    if not is_query_on_topic(query_en):
        polite_msg = "I can only help with questions related to farming, weather/temperature, market prices, and government schemes. Please ask a question related to these topics."
        if language != "English":
            try:
                polite_msg = translate_text(polite_msg, target_language=language)
            except Exception as e:
                logger.warning(f"Failed to translate polite message: {e}")

        return {
            "answer": polite_msg,
            "sources": [],
            "retrieved_docs": 0,
            "language": language,
            "intent": "out_of_scope",
            "cached": False,
            "live_data": None
        }

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
    if soil_ph is not None:
        context_parts.append(f"Soil pH: {soil_ph}")
    if npk_nitrogen is not None or npk_phosphorus is not None or npk_potassium is not None:
        context_parts.append(f"NPK: N={npk_nitrogen or 0} P={npk_phosphorus or 0} K={npk_potassium or 0}")
    if farm_size is not None:
        context_parts.append(f"Farm size: {farm_size} acres")
    if irrigation:
        context_parts.append(f"Irrigation: {irrigation}")
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
