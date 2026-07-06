"""
API Router: Weather
"""
import logging
from fastapi import APIRouter, HTTPException, Query

from modules.weather import get_weather_summary

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/current")
async def current_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    """Get current weather and 7-day forecast for a location."""
    try:
        data = await get_weather_summary(lat, lon)
        return data
    except Exception as e:
        logger.error(f"Weather error: {e}")
        raise HTTPException(status_code=502, detail=f"Weather data unavailable: {e}")


# Preset coordinates for major Indian cities
CITY_COORDS = {
    "delhi":     (28.6139, 77.2090),
    "mumbai":    (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai":   (13.0827, 80.2707),
    "kolkata":   (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "pune":      (18.5204, 73.8567),
    "ahmedabad": (23.0225, 72.5714),
    "jaipur":    (26.9124, 75.7873),
    "lucknow":   (26.8467, 80.9462),
    "patna":     (25.5941, 85.1376),
    "bhopal":    (23.2599, 77.4126),
    "nagpur":    (21.1458, 79.0882),
    "chandigarh":(30.7333, 76.7794),
    "indore":    (22.7196, 75.8577),
}


@router.get("/city/{city_name}")
async def weather_by_city(city_name: str):
    """Get weather for a preset Indian city."""
    city_key = city_name.lower().strip()
    if city_key not in CITY_COORDS:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city_name}' not in presets. Use /current?lat=...&lon=... instead.",
        )
    lat, lon = CITY_COORDS[city_key]
    data = await get_weather_summary(lat, lon)
    data["city"] = city_name.capitalize()
    return data


@router.get("/cities")
async def list_cities():
    """List available preset cities."""
    return [{"name": k.capitalize(), "lat": v[0], "lon": v[1]} for k, v in CITY_COORDS.items()]
