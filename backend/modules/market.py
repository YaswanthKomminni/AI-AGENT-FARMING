"""
Module: Mandi/Market Prices — data.gov.in API + fallback demo data
"""
import logging
from typing import Optional

import httpx
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Demo data for when API is unavailable
DEMO_PRICES = {
    "wheat":    [{"commodity": "Wheat",    "market": "Delhi",    "modal_price": "2200", "state": "Delhi"},
                 {"commodity": "Wheat",    "market": "Kanpur",   "modal_price": "2150", "state": "UP"}],
    "rice":     [{"commodity": "Rice",     "market": "Patna",    "modal_price": "3500", "state": "Bihar"},
                 {"commodity": "Rice",     "market": "Cuttack",  "modal_price": "3400", "state": "Odisha"}],
    "onion":    [{"commodity": "Onion",    "market": "Lasalgaon","modal_price": "1800", "state": "Maharashtra"},
                 {"commodity": "Onion",    "market": "Pune",     "modal_price": "2000", "state": "Maharashtra"}],
    "tomato":   [{"commodity": "Tomato",   "market": "Kolar",    "modal_price": "2500", "state": "Karnataka"},
                 {"commodity": "Tomato",   "market": "Nashik",   "modal_price": "2200", "state": "Maharashtra"}],
    "cotton":   [{"commodity": "Cotton",   "market": "Akola",    "modal_price": "6500", "state": "Maharashtra"},
                 {"commodity": "Cotton",   "market": "Rajkot",   "modal_price": "6800", "state": "Gujarat"}],
    "potato":   [{"commodity": "Potato",   "market": "Agra",     "modal_price": "1200", "state": "UP"},
                 {"commodity": "Potato",   "market": "Kolkata",  "modal_price": "1400", "state": "WB"}],
    "soybean":  [{"commodity": "Soybean",  "market": "Indore",   "modal_price": "4200", "state": "MP"},
                 {"commodity": "Soybean",  "market": "Nagpur",   "modal_price": "4100", "state": "Maharashtra"}],
    "maize":    [{"commodity": "Maize",    "market": "Davangere","modal_price": "1900", "state": "Karnataka"},
                 {"commodity": "Maize",    "market": "Nizamabad","modal_price": "1850", "state": "Telangana"}],
}


async def get_market_prices(commodity: str = "wheat", state: Optional[str] = None) -> list[dict]:
    """
    Fetch live mandi prices from data.gov.in API.
    Falls back to demo data if API key is not configured or request fails.
    """
    if not settings.mandi_api_key or settings.mandi_api_key == "your_mandi_api_key_here":
        logger.info("Mandi API key not configured — using demo data")
        return _get_demo_prices(commodity)

    try:
        params = {
            "api-key": settings.mandi_api_key,
            "format": "json",
            "filters[commodity]": commodity.capitalize(),
            "limit": 10,
        }
        if state:
            params["filters[state]"] = state

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(settings.mandi_api_base_url, params=params)
            response.raise_for_status()
            data = response.json()

        records = data.get("records", [])
        return [
            {
                "commodity": r.get("commodity", ""),
                "market": r.get("market", ""),
                "state": r.get("state", ""),
                "min_price": r.get("min_price", ""),
                "max_price": r.get("max_price", ""),
                "modal_price": r.get("modal_price", ""),
                "date": r.get("arrival_date", ""),
            }
            for r in records
        ]
    except Exception as e:
        logger.warning(f"Mandi API error: {e}. Using demo data.")
        return _get_demo_prices(commodity)


def _get_demo_prices(commodity: str) -> list[dict]:
    """Return demo prices for common crops."""
    key = commodity.lower()
    return DEMO_PRICES.get(key, [
        {"commodity": commodity.capitalize(), "market": "Sample Market",
         "modal_price": "2000", "state": "India",
         "note": "Demo data — configure MANDI_API_KEY for live prices"},
    ])
