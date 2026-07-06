"""
Module: Pest and Disease Diagnosis
"""
from typing import Optional

PEST_DATABASE = {
    "yellow_spots": {
        "name": "Leaf spot / Yellow mosaic virus",
        "crops_affected": ["Tomato", "Soybean", "Mung bean", "Papaya"],
        "cause": "Fungal infection or viral disease spread by whiteflies",
        "symptoms": ["Yellow circular spots", "Mosaic pattern", "Leaf distortion"],
        "prevention": [
            "Use certified disease-free seeds",
            "Spray neem oil (3%) at early stage",
            "Remove and destroy infected plant parts",
            "Use reflective mulch to repel whiteflies",
        ],
        "treatment": [
            "Mancozeb 0.25% spray every 7 days",
            "Carbendazim 0.1% for fungal control",
            "Control whiteflies with Imidacloprid 0.005%",
        ],
        "organic": ["Neem oil spray (5ml/L)", "Trichoderma viride soil application"],
        "severity": "Medium",
    },
    "white_powder": {
        "name": "Powdery Mildew",
        "crops_affected": ["Wheat", "Peas", "Cucurbits", "Grapes"],
        "cause": "Fungus Erysiphe spp. in dry conditions with high humidity",
        "symptoms": ["White powdery coating on leaves", "Yellowing", "Premature leaf drop"],
        "prevention": [
            "Avoid excessive nitrogen fertilizer",
            "Ensure good air circulation",
            "Use resistant varieties",
        ],
        "treatment": [
            "Sulfur-based fungicide (0.3%) spray",
            "Hexaconazole 0.05% spray",
            "Propiconazole 0.1% spray",
        ],
        "organic": ["Baking soda solution (1 tsp/L)", "Milk spray (1:10 dilution)"],
        "severity": "Medium",
    },
    "wilting": {
        "name": "Fusarium Wilt / Root Rot",
        "crops_affected": ["Cotton", "Tomato", "Banana", "Pulses"],
        "cause": "Soil-borne fungus Fusarium oxysporum",
        "symptoms": ["Sudden wilting", "Brown discoloration of stem base", "Root decay"],
        "prevention": [
            "Crop rotation every 2–3 years",
            "Use Trichoderma-treated seeds",
            "Avoid waterlogging",
            "Soil solarization before planting",
        ],
        "treatment": [
            "Drench with Carbendazim 0.1%",
            "Apply Trichoderma viride 5g/kg soil",
        ],
        "organic": ["Neem cake application (250 kg/ha)", "Trichoderma enriched compost"],
        "severity": "High",
    },
    "stem_borer": {
        "name": "Stem Borer",
        "crops_affected": ["Rice", "Maize", "Sugarcane", "Sorghum"],
        "cause": "Larvae of Scirpophaga spp. or Chilo suppressalis",
        "symptoms": ["Dead heart in vegetative stage", "White ears at grain filling", "Entry holes in stems"],
        "prevention": [
            "Use light traps to catch adults",
            "Release Trichogramma egg parasitoid",
            "Clip tips of seedlings before transplanting",
        ],
        "treatment": [
            "Chlorpyrifos 20 EC @ 2.5 ml/L spray",
            "Cartap hydrochloride 4G @ 8 kg/ha granules",
            "Coragen (Chlorantraniliprole) 0.5 ml/L",
        ],
        "organic": ["Neem seed kernel extract (5%)", "Bacillus thuringiensis spray"],
        "severity": "High",
    },
    "aphids": {
        "name": "Aphids",
        "crops_affected": ["Mustard", "Wheat", "Vegetables", "Cotton"],
        "cause": "Small sap-sucking insects; often colony-forming",
        "symptoms": ["Curled leaves", "Sticky honeydew", "Stunted growth", "Sooty mold"],
        "prevention": [
            "Conserve natural enemies (ladybirds, lacewings)",
            "Avoid over-fertilization with nitrogen",
            "Use yellow sticky traps",
        ],
        "treatment": [
            "Imidacloprid 0.3 ml/L spray",
            "Dimethoate 30 EC @ 1.5 ml/L",
        ],
        "organic": ["Neem oil 5ml/L spray", "Garlic-chili extract spray"],
        "severity": "Low-Medium",
    },
}

SYMPTOM_KEYWORDS = {
    "yellow_spots":  ["yellow spot", "yellow patch", "mosaic", "yellow leaf"],
    "white_powder":  ["white powder", "powdery", "white coating"],
    "wilting":       ["wilt", "drooping", "collapse", "dying", "brown stem"],
    "stem_borer":    ["stem borer", "dead heart", "hole in stem", "white ear"],
    "aphids":        ["aphid", "sticky", "curled leaf", "sooty"],
}


def diagnose_pest(symptoms: str, crop: Optional[str] = None) -> dict:
    """
    Match symptoms to pest/disease database.
    Returns diagnosis + treatment plan.
    """
    symptoms_lower = symptoms.lower()
    matches = []

    for pest_key, keywords in SYMPTOM_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in symptoms_lower)
        if score > 0:
            matches.append((score, pest_key))

    if not matches:
        return {
            "diagnosis": "Unknown",
            "confidence": "Low",
            "message": (
                "Could not identify a specific pest or disease from the symptoms described. "
                "Please consult your local Krishi Vigyan Kendra (KVK) or state agriculture department."
            ),
            "general_advice": [
                "Collect a sample of affected plant parts",
                "Photograph the symptoms for expert consultation",
                "Check nearby farms for similar symptoms",
            ],
        }

    # Best match
    matches.sort(reverse=True)
    best_key = matches[0][1]
    pest_info = PEST_DATABASE[best_key]

    # Filter by crop if provided
    if crop and crop not in pest_info.get("crops_affected", []):
        for _, key in matches[1:]:
            alt = PEST_DATABASE[key]
            if crop in alt.get("crops_affected", []):
                pest_info = alt
                best_key = key
                break

    return {
        "diagnosis": pest_info["name"],
        "severity": pest_info["severity"],
        "confidence": "High" if matches[0][0] >= 2 else "Medium",
        "cause": pest_info["cause"],
        "symptoms_matched": pest_info["symptoms"],
        "prevention": pest_info["prevention"],
        "chemical_treatment": pest_info["treatment"],
        "organic_treatment": pest_info["organic"],
        "crops_affected": pest_info["crops_affected"],
        "safety_note": (
            "⚠️ Always wear protective equipment (gloves, mask) when applying pesticides. "
            "Follow label instructions and observe pre-harvest intervals (PHI)."
        ),
    }
