"""
API Router: Market Prices
"""
import logging
from typing import Optional
from fastapi import APIRouter, Query

from modules.market import get_market_prices

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/prices")
async def market_prices(
    commodity: str = Query("wheat", description="Crop/commodity name"),
    state: Optional[str] = Query(None, description="State name"),
):
    """Get mandi prices for a commodity."""
    prices = await get_market_prices(commodity=commodity, state=state)
    return {
        "commodity": commodity,
        "state": state,
        "prices": prices,
        "count": len(prices),
        "note": "Prices in ₹/quintal. Source: data.gov.in / demo data.",
    }


@router.get("/commodities")
async def list_commodities():
    """List supported commodities for price lookup."""
    return {
        "commodities": [
            "wheat", "rice", "maize", "cotton", "soybean",
            "onion", "tomato", "potato", "sugarcane",
            "mustard", "arhar", "moong", "chana",
        ]
    }
