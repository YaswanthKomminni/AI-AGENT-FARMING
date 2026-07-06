"""
Module: Fertilizer Recommendations
"""
from typing import Optional

FERTILIZER_DATABASE = {
    "rice": {
        "npk_recommendation": {"N": 120, "P": 60, "K": 60},
        "unit": "kg/ha",
        "schedule": [
            "Basal (at transplanting): Full P + K + 1/3 N",
            "Tillering (20–25 days): 1/3 N (top dressing)",
            "Panicle initiation (45–50 days): 1/3 N (top dressing)",
        ],
        "micronutrients": ["Zinc sulfate 25 kg/ha if deficiency observed"],
        "organic": ["FYM 10 ton/ha 3 weeks before transplanting", "Green manure (Sesbania)"],
        "biofertilizers": ["Azolla as green manure", "BGA (Blue Green Algae) 10 kg/ha"],
    },
    "wheat": {
        "npk_recommendation": {"N": 120, "P": 60, "K": 40},
        "unit": "kg/ha",
        "schedule": [
            "Basal: Full P + K + 1/2 N",
            "Crown root initiation (20–25 DAS): 1/2 N (top dressing)",
        ],
        "micronutrients": ["Sulfur 20 kg/ha", "Zinc 25 kg/ha"],
        "organic": ["FYM 8–10 ton/ha", "Vermicompost 5 ton/ha"],
        "biofertilizers": ["Azatobacter 5 kg/ha", "PSB 5 kg/ha"],
    },
    "cotton": {
        "npk_recommendation": {"N": 160, "P": 80, "K": 80},
        "unit": "kg/ha",
        "schedule": [
            "Basal: Full P + K + 1/2 N",
            "45 days: 1/4 N",
            "75 days: 1/4 N (boll formation)",
        ],
        "micronutrients": ["Boron 1 kg/ha", "Zinc 25 kg/ha"],
        "organic": ["FYM 15 ton/ha", "Neem cake 400 kg/ha"],
        "biofertilizers": ["Azatobacter + PSB seed treatment"],
    },
    "tomato": {
        "npk_recommendation": {"N": 180, "P": 100, "K": 100},
        "unit": "kg/ha",
        "schedule": [
            "Transplanting: Full P + K + 1/3 N",
            "25 days: 1/3 N",
            "45 days (flowering): 1/3 N + foliar K",
        ],
        "micronutrients": ["Calcium nitrate 1% foliar spray at fruiting", "Magnesium sulfate foliar"],
        "organic": ["Vermicompost 8 ton/ha", "Poultry manure 5 ton/ha"],
        "biofertilizers": ["Trichoderma soil application"],
    },
    "maize": {
        "npk_recommendation": {"N": 150, "P": 75, "K": 75},
        "unit": "kg/ha",
        "schedule": [
            "Basal: Full P + K + 1/3 N",
            "V4 stage (4 leaves): 1/3 N",
            "Tasseling: 1/3 N",
        ],
        "micronutrients": ["Zinc 25 kg/ha"],
        "organic": ["FYM 8 ton/ha"],
        "biofertilizers": ["Azatobacter 5 kg/ha"],
    },
}

NUTRIENT_DEFICIENCY_SYMPTOMS = {
    "nitrogen": {
        "symptoms": "Yellowing starts from older/lower leaves; stunted growth",
        "source": "Urea (46% N), DAP (18% N), CAN",
        "organic": "FYM, compost, poultry manure",
    },
    "phosphorus": {
        "symptoms": "Purple/reddish leaf undersides; poor root development; delayed maturity",
        "source": "DAP (46% P2O5), SSP (16% P2O5), TSP",
        "organic": "Rock phosphate, bone meal",
    },
    "potassium": {
        "symptoms": "Leaf margin/tip burn (scorching); weak stems; poor fruit quality",
        "source": "MOP (60% K2O), SOP (50% K2O)",
        "organic": "Wood ash, banana peel compost",
    },
    "zinc": {
        "symptoms": "Interveinal chlorosis; small leaves; bronze/khaki patches in rice (Khaira disease)",
        "source": "Zinc sulfate 21% or 33%",
        "dose": "25–50 kg/ha soil application or 0.5% foliar spray",
    },
    "iron": {
        "symptoms": "Interveinal yellowing starting from young leaves",
        "source": "Ferrous sulfate 19%",
        "dose": "0.5% foliar spray × 3 times",
    },
}


def get_fertilizer_advice(
    crop: str,
    area_ha: float = 1.0,
    deficiency: Optional[str] = None,
) -> dict:
    """Returns fertilizer schedule and deficiency treatment for a crop."""
    crop_key = crop.lower().strip()
    data = FERTILIZER_DATABASE.get(crop_key)

    if not data:
        return {
            "crop": crop,
            "message": f"Specific fertilizer data not found for '{crop}'. Using general guidelines.",
            "general_npk": {"N": 100, "P": 50, "K": 50},
            "unit": "kg/ha",
            "advice": "Get a Soil Health Card (SHC) test for precise fertilizer recommendations.",
        }

    # Scale NPK by area
    npk_total = {
        nutrient: round(val * area_ha)
        for nutrient, val in data["npk_recommendation"].items()
    }

    result = {
        "crop": crop,
        "area_ha": area_ha,
        "npk_recommendation_kg_per_ha": data["npk_recommendation"],
        "total_fertilizer_required_kg": npk_total,
        "application_schedule": data["schedule"],
        "micronutrients": data["micronutrients"],
        "organic_options": data["organic"],
        "biofertilizers": data["biofertilizers"],
        "soil_test_note": "Always base fertilizer use on Soil Health Card (SHC) results for precision nutrition.",
    }

    # Add deficiency info if provided
    if deficiency:
        def_key = deficiency.lower()
        if def_key in NUTRIENT_DEFICIENCY_SYMPTOMS:
            result["deficiency_treatment"] = NUTRIENT_DEFICIENCY_SYMPTOMS[def_key]

    return result
