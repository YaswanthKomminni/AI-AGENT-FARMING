"""
Module: Crop Recommendations
"""
from typing import Optional


CROP_DATABASE = {
    "alluvial": {
        "kharif": ["Rice", "Jute", "Sugarcane", "Maize", "Cotton"],
        "rabi":   ["Wheat", "Barley", "Mustard", "Chickpea"],
        "zaid":   ["Watermelon", "Cucumber", "Muskmelon"],
    },
    "black": {
        "kharif": ["Cotton", "Soybean", "Sorghum", "Pigeon pea"],
        "rabi":   ["Wheat", "Chickpea", "Safflower", "Sunflower"],
        "zaid":   ["Moong", "Groundnut"],
    },
    "red": {
        "kharif": ["Millets", "Groundnut", "Maize", "Rice"],
        "rabi":   ["Wheat", "Barley", "Mustard"],
        "zaid":   ["Vegetables", "Gourds"],
    },
    "laterite": {
        "kharif": ["Rice", "Cashew", "Tea", "Coffee", "Rubber"],
        "rabi":   ["Vegetables", "Pulses"],
        "zaid":   ["Vegetables"],
    },
    "sandy": {
        "kharif": ["Pearl millet (Bajra)", "Cluster bean", "Moth bean"],
        "rabi":   ["Mustard", "Wheat", "Barley"],
        "zaid":   ["Watermelon", "Cucumber"],
    },
}

SEASON_CROPS = {
    "kharif": ["Rice", "Maize", "Cotton", "Soybean", "Groundnut", "Bajra", "Jowar", "Arhar"],
    "rabi":   ["Wheat", "Barley", "Mustard", "Chickpea", "Lentil", "Oat", "Sunflower"],
    "zaid":   ["Watermelon", "Cucumber", "Moong", "Vegetables"],
}


def get_crop_recommendation(
    soil_type: Optional[str] = None,
    season: Optional[str] = None,
    state: Optional[str] = None,
    rainfall: Optional[float] = None,
    temperature: Optional[float] = None,
) -> dict:
    """
    Returns crop recommendations based on soil, season, and climate.
    """
    soil_key = (soil_type or "alluvial").lower().replace(" ", "_")
    season_key = (season or "kharif").lower()

    # Normalize soil names
    for key in CROP_DATABASE:
        if key in soil_key:
            soil_key = key
            break
    else:
        soil_key = "alluvial"

    if season_key not in ("kharif", "rabi", "zaid"):
        season_key = "kharif"

    crops = CROP_DATABASE.get(soil_key, CROP_DATABASE["alluvial"]).get(season_key, [])

    # Filter by rainfall if provided
    if rainfall is not None:
        if rainfall < 300:
            crops = [c for c in crops if c in ["Pearl millet (Bajra)", "Cluster bean", "Moth bean", "Mustard", "Barley"]]
        elif rainfall > 1500:
            crops = [c for c in crops if c not in ["Bajra", "Mustard", "Barley"]]

    return {
        "recommended_crops": crops,
        "soil_type": soil_key,
        "season": season_key,
        "state": state,
        "notes": (
            f"These crops are recommended for {soil_key} soil during {season_key} season. "
            "Consult your local KVK for variety-specific guidance."
        ),
    }
