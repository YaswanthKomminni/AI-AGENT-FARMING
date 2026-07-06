"""
API Router: Government Schemes
"""
from fastapi import APIRouter, Query
from typing import Optional
from modules.schemes import get_relevant_schemes, search_schemes

router = APIRouter()


@router.get("/list")
async def list_schemes(
    category: Optional[str] = Query(None, description="Filter by category"),
    state: Optional[str] = Query(None, description="Filter by state"),
):
    """List government schemes for farmers."""
    schemes = get_relevant_schemes(category=category, state=state)
    return {"schemes": schemes, "count": len(schemes)}


@router.get("/search")
async def search(q: str = Query(..., description="Search keyword")):
    """Search schemes by keyword."""
    results = search_schemes(q)
    return {"results": results, "count": len(results)}


@router.get("/categories")
async def categories():
    return {
        "categories": [
            "income_support", "insurance", "credit", "irrigation",
            "organic_farming", "mechanization", "soil_health", "market",
        ]
    }
