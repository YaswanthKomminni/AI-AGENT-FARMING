"""
Module: Irrigation Guidance
"""
from typing import Optional

IRRIGATION_DATA = {
    "rice": {
        "water_requirement_mm": "1200–2000",
        "method": "Flooded / Alternate Wetting & Drying (AWD)",
        "schedule": [
            "Puddling: Flood field 5–7 days before transplanting",
            "Vegetative: Maintain 5 cm standing water",
            "AWD: Let water level drop to 15 cm below surface, then re-irrigate",
            "Flowering: Ensure continuous flooding",
            "Ripening: Stop irrigation 10 days before harvest",
        ],
        "conservation": [
            "AWD method saves 15–30% water compared to continuous flooding",
            "System of Rice Intensification (SRI) reduces water use by 40%",
        ],
    },
    "wheat": {
        "water_requirement_mm": "400–500",
        "method": "Furrow / Sprinkler",
        "schedule": [
            "Crown Root Initiation (CRI): 20–25 days after sowing",
            "Tillering: 40–45 DAS",
            "Jointing: 60–65 DAS",
            "Flowering: 80–85 DAS",
            "Grain filling: 100–105 DAS",
            "Dough stage: 115–120 DAS",
        ],
        "conservation": [
            "Sprinkler irrigation saves 30–40% water",
            "Laser land leveling reduces water wastage",
        ],
    },
    "cotton": {
        "water_requirement_mm": "700–1200",
        "method": "Drip / Furrow",
        "schedule": [
            "Pre-sowing irrigation: 10–15 cm depth",
            "Vegetative stage: Irrigate every 10–12 days",
            "Boll development: Critical period — irrigate every 8–10 days",
            "Boll opening: Reduce irrigation frequency",
        ],
        "conservation": [
            "Drip irrigation saves 40–50% water and increases yield by 20–30%",
            "Mulching reduces soil evaporation",
        ],
    },
    "maize": {
        "water_requirement_mm": "500–800",
        "method": "Furrow / Drip",
        "schedule": [
            "Germination: Keep soil moist but not waterlogged",
            "Knee height: Irrigate every 7–8 days",
            "Tasseling/Silking: Critical stage — irrigate every 5 days",
            "Grain filling: Every 8–10 days",
        ],
        "conservation": [
            "Avoid water stress during tasseling — reduces yield by 40%",
            "Ridges and furrow system reduces evaporation",
        ],
    },
    "tomato": {
        "water_requirement_mm": "400–600",
        "method": "Drip / Sprinkler",
        "schedule": [
            "Seedling: Light frequent irrigation",
            "Vegetative: Every 4–5 days",
            "Flowering: Every 3 days (critical stage)",
            "Fruit development: Every 4 days",
        ],
        "conservation": [
            "Drip fertigation (fertilizer through drip) increases yield and reduces water by 40%",
            "Mulching with black plastic reduces moisture loss",
        ],
    },
}


def get_irrigation_advice(
    crop: str,
    area_ha: float = 1.0,
    method: Optional[str] = None,
) -> dict:
    """Returns irrigation schedule and water requirements for a crop."""
    crop_key = crop.lower().strip()
    data = IRRIGATION_DATA.get(crop_key, None)

    if not data:
        return {
            "crop": crop,
            "message": f"Irrigation data not found for '{crop}'. Please consult your local agriculture office.",
            "general_tips": [
                "Irrigate based on soil moisture, not on a fixed schedule",
                "Check soil moisture 15 cm deep before irrigating",
                "Irrigate early morning or evening to reduce evaporation losses",
            ],
        }

    # Estimate total water volume (simplified)
    water_range = data["water_requirement_mm"].split("–")
    avg_mm = (int(water_range[0]) + int(water_range[-1])) // 2
    water_volume_m3 = avg_mm * 10 * area_ha  # 1 mm/ha = 10 m³

    return {
        "crop": crop,
        "area_ha": area_ha,
        "water_requirement_mm_season": data["water_requirement_mm"],
        "estimated_total_water_m3": water_volume_m3,
        "recommended_method": method or data["method"],
        "irrigation_schedule": data["schedule"],
        "conservation_tips": data["conservation"],
        "note": "Actual water needs may vary based on rainfall, soil type, and local climate.",
    }
