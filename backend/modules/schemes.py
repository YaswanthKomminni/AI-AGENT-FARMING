"""
Module: Government Schemes for Farmers
"""
from typing import Optional

SCHEMES_DATABASE = [
    {
        "id": "pm-kisan",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "benefit": "₹6,000 per year in 3 equal installments of ₹2,000",
        "eligibility": [
            "Small and marginal farmers with cultivable land up to 2 hectares",
            "Indian citizen",
            "Not a government employee or income taxpayer",
        ],
        "documents": ["Aadhaar card", "Land records / Khatoni", "Bank account"],
        "apply_at": "PM-KISAN portal (pmkisan.gov.in) or Common Service Centre (CSC)",
        "category": "income_support",
    },
    {
        "id": "pmfby",
        "name": "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
        "benefit": "Crop insurance — full coverage against natural calamities, pests, diseases",
        "premium": "2% for Kharif, 1.5% for Rabi, 5% for Horticulture",
        "eligibility": [
            "All farmers — loanee and non-loanee",
            "Both small/marginal and large farmers",
        ],
        "documents": ["Aadhaar card", "Bank account", "Land records", "Sowing certificate"],
        "apply_at": "Nearest bank, insurance company, or online at pmfby.gov.in",
        "deadline": "Within 2 weeks of sowing",
        "category": "insurance",
    },
    {
        "id": "kcc",
        "name": "KCC (Kisan Credit Card)",
        "benefit": "Short-term agricultural credit at 4% interest (with timely repayment)",
        "credit_limit": "Based on land holding and crop pattern",
        "eligibility": [
            "Farmers with land ownership or tenancy",
            "Sharecroppers and oral lessees also eligible",
        ],
        "documents": ["Aadhaar", "Land records", "PAN / Passport photo"],
        "apply_at": "Any nationalized bank, cooperative bank, or RRB",
        "category": "credit",
    },
    {
        "id": "pmksy",
        "name": "PMKSY (Pradhan Mantri Krishi Sinchayee Yojana)",
        "benefit": "Subsidy on drip and sprinkler irrigation equipment (40–90% subsidy)",
        "eligibility": [
            "All categories of farmers",
            "SC/ST/small farmers get higher subsidy",
        ],
        "documents": ["Aadhaar", "Land records", "Bank account"],
        "apply_at": "State Agriculture Department or District Horticulture office",
        "category": "irrigation",
    },
    {
        "id": "pkvy",
        "name": "PKVY (Paramparagat Krishi Vikas Yojana)",
        "benefit": "₹50,000/ha for 3 years for organic farming transition",
        "eligibility": [
            "Farmers forming clusters of 50+ for organic farming",
            "No previous organic certification required",
        ],
        "documents": ["Aadhaar", "Land records", "Group formation deed"],
        "apply_at": "Nearby Krishi Vigyan Kendra (KVK) or State Agriculture Dept",
        "category": "organic_farming",
    },
    {
        "id": "smam",
        "name": "SMAM (Sub-Mission on Agricultural Mechanization)",
        "benefit": "25–50% subsidy on farm machinery (tractors, power tillers, harvesters)",
        "eligibility": [
            "SC/ST: 50% subsidy",
            "Small/Marginal/Women farmers: 40–50% subsidy",
            "Others: 25% subsidy",
        ],
        "documents": ["Aadhaar", "Caste certificate (if applicable)", "Land records"],
        "apply_at": "State Department of Agriculture or online portal",
        "category": "mechanization",
    },
    {
        "id": "soil-health-card",
        "name": "Soil Health Card Scheme",
        "benefit": "Free soil testing and customized fertilizer recommendations",
        "eligibility": ["All farmers"],
        "documents": ["Aadhaar or any ID", "Land location details"],
        "apply_at": "Nearest Soil Testing Laboratory or Agriculture Department",
        "category": "soil_health",
    },
    {
        "id": "e-nam",
        "name": "e-NAM (National Agriculture Market)",
        "benefit": "Online mandi platform — sell crops across India at best prices",
        "eligibility": ["All farmers with produce to sell"],
        "documents": ["Aadhaar", "Bank account", "Mobile number"],
        "apply_at": "enam.gov.in or nearest APMC market",
        "category": "market",
    },
]


def get_relevant_schemes(
    category: Optional[str] = None,
    farmer_type: Optional[str] = None,
    state: Optional[str] = None,
) -> list[dict]:
    """Return schemes filtered by category/farmer type."""
    schemes = SCHEMES_DATABASE

    if category:
        category_lower = category.lower()
        schemes = [
            s for s in schemes
            if category_lower in s.get("category", "") or category_lower in s["name"].lower()
        ]

    return schemes if schemes else SCHEMES_DATABASE


def search_schemes(query: str) -> list[dict]:
    """Search schemes by keyword."""
    query_lower = query.lower()
    results = []
    keywords = ["insurance", "loan", "credit", "subsidy", "income", "organic",
                 "irrigation", "machinery", "market", "soil", "water", "scheme"]

    for scheme in SCHEMES_DATABASE:
        if (
            any(kw in query_lower for kw in [scheme["id"], scheme["name"].lower()])
            or any(kw in query_lower for kw in keywords and kw in scheme["category"])
        ):
            results.append(scheme)

    return results if results else SCHEMES_DATABASE[:4]
