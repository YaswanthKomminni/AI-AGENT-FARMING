"""
IBM Granite LLM — Watsonx.ai Integration
"""
import logging
from functools import lru_cache

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@lru_cache
def get_granite_llm():
    """
    Returns a LangChain-compatible IBM Watsonx Granite LLM.
    Falls back to a mock if credentials are not configured.
    Supported on IBM Cloud Lite: ibm/granite-3-1-8b-base, ibm/granite-4-h-small
    """
    if not settings.ibm_watsonx_api_key or settings.ibm_watsonx_api_key == "your_ibm_watsonx_api_key_here":
        logger.warning("IBM Watsonx credentials not configured — using MockLLM")
        return _MockGraniteLLM()

    try:
        from langchain_ibm import WatsonxLLM
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

        llm = WatsonxLLM(
            model_id=settings.ibm_granite_model_id,
            url=settings.ibm_watsonx_url,
            apikey=settings.ibm_watsonx_api_key,
            project_id=settings.ibm_watsonx_project_id,
            params={
                GenParams.MAX_NEW_TOKENS: 400,   # reduced: 800→400 for 2x faster responses
                GenParams.TEMPERATURE: 0.3,
                GenParams.TOP_P: 0.9,
                GenParams.TOP_K: 50,
                GenParams.REPETITION_PENALTY: 1.1,
            },
        )
        logger.info(f"IBM Granite (WatsonxLLM) initialised: {settings.ibm_granite_model_id}")
        return llm
    except Exception as e:
        logger.error(f"Failed to initialise IBM Granite LLM: {e}", exc_info=True)
        return _MockGraniteLLM()


class _MockGraniteLLM:
    """
    Development mock that returns structured demo responses
    when IBM Watsonx credentials are not yet configured.
    """

    def invoke(self, prompt: str) -> str:
        query_lower = prompt.lower()

        if any(k in query_lower for k in ["crop", "grow", "plant", "season"]):
            return (
                "**Crop Recommendation (Demo Mode)**\n\n"
                "Based on the season and typical soil conditions:\n"
                "- **Kharif (June–Oct):** Rice, Maize, Cotton, Soybean, Groundnut\n"
                "- **Rabi (Nov–Mar):** Wheat, Mustard, Chickpea, Barley\n"
                "- **Zaid (Apr–Jun):** Watermelon, Cucumber, Moong Dal\n\n"
                "**Recommendation:** Choose crops suited to your local soil type. "
                "Sandy loam soils work well for most cereals. Black cotton soil is ideal for cotton.\n\n"
                "_Note: Connect IBM Watsonx credentials for personalized AI recommendations._"
            )
        elif any(k in query_lower for k in ["pest", "disease", "yellow", "spot", "insect"]):
            return (
                "**Pest & Disease Advisory (Demo Mode)**\n\n"
                "Common symptoms and treatments:\n"
                "- **Yellow spots on leaves:** Likely fungal infection or nutrient deficiency\n"
                "  - Treatment: Mancozeb 0.25% spray; check soil pH\n"
                "- **White powder on leaves:** Powdery mildew\n"
                "  - Treatment: Sulfur-based fungicide; improve air circulation\n"
                "- **Wilting plants:** Root rot or water stress\n"
                "  - Treatment: Improve drainage; reduce irrigation\n\n"
                "⚠️ _Always follow label instructions for pesticide use. Wear protective equipment._"
            )
        elif any(k in query_lower for k in ["fertilizer", "nutrient", "npk", "urea"]):
            return (
                "**Fertilizer Recommendation (Demo Mode)**\n\n"
                "General NPK guidelines:\n"
                "- **Rice:** N:P:K = 120:60:60 kg/ha\n"
                "- **Wheat:** N:P:K = 120:60:40 kg/ha\n"
                "- **Cotton:** N:P:K = 160:80:80 kg/ha\n\n"
                "**Organic Alternatives:**\n"
                "- Vermicompost: 5 ton/ha\n"
                "- Green manure (Dhaincha): 3 weeks before transplanting\n"
                "- Biofertilizers: Rhizobium, PSB, Azatobacter\n\n"
                "_Get a soil health card test for precise recommendations._"
            )
        elif any(k in query_lower for k in ["water", "irrigation", "drip"]):
            return (
                "**Irrigation Guidance (Demo Mode)**\n\n"
                "Water requirements by crop:\n"
                "- **Rice:** 1200–2000 mm/season; continuous flooding or AWD method\n"
                "- **Wheat:** 400–500 mm; 4–6 irrigations\n"
                "- **Cotton:** 700–1200 mm; drip irrigation saves 40% water\n\n"
                "**Water Conservation Tips:**\n"
                "1. Use drip/sprinkler irrigation\n"
                "2. Mulching reduces evaporation by 30%\n"
                "3. Irrigate early morning or evening\n"
                "4. Check soil moisture before irrigating"
            )
        elif any(k in query_lower for k in ["scheme", "subsidy", "loan", "insurance", "pm-kisan"]):
            return (
                "**Government Schemes (Demo Mode)**\n\n"
                "Key schemes for farmers:\n"
                "- **PM-KISAN:** ₹6,000/year for small/marginal farmers\n"
                "- **PMFBY:** Pradhan Mantri Fasal Bima Yojana — crop insurance at low premiums\n"
                "- **KCC:** Kisan Credit Card — short-term credit at 4% interest\n"
                "- **PKVY:** Organic farming support scheme\n"
                "- **SMAM:** Subsidies on agricultural machinery\n\n"
                "_Contact your local Krishi Vigyan Kendra (KVK) for eligibility and application._"
            )
        else:
            return (
                "**FarmWise AI (Demo Mode)**\n\n"
                "I can help you with:\n"
                "🌾 Crop selection and recommendations\n"
                "🪲 Pest and disease identification\n"
                "🌱 Fertilizer and nutrient management\n"
                "💧 Irrigation planning\n"
                "📢 Government schemes and subsidies\n"
                "💰 Market prices and selling advice\n\n"
                "Please ask a specific farming question!\n\n"
                "_Connect IBM Watsonx API key for full AI-powered responses._"
            )
