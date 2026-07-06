"""
Module: Real-time Weather using Open-Meteo API (free, no API key needed)
"""
import logging
from typing import Optional

import httpx
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Heavy drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail",
}


async def get_weather_summary(lat: float, lon: float) -> dict:
    """Fetch current weather + 7-day forecast from Open-Meteo."""
    url = f"{settings.weather_api_base_url}/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "precipitation", "weather_code", "wind_speed_10m",
        ],
        "daily": [
            "temperature_2m_max", "temperature_2m_min",
            "precipitation_sum", "weather_code",
        ],
        "timezone": "Asia/Kolkata",
        "forecast_days": 7,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    current = data.get("current", {})
    daily = data.get("daily", {})

    # Build 7-day forecast
    forecast = []
    dates = daily.get("time", [])
    for i, date in enumerate(dates):
        forecast.append({
            "date": date,
            "max_temp": daily["temperature_2m_max"][i],
            "min_temp": daily["temperature_2m_min"][i],
            "precipitation": daily["precipitation_sum"][i],
            "condition": WMO_CODES.get(daily["weather_code"][i], "Unknown"),
        })

    # Farming advisory
    advisory = _generate_weather_advisory(current, forecast)

    return {
        "current": {
            "temperature_2m": current.get("temperature_2m"),
            "relative_humidity_2m": current.get("relative_humidity_2m"),
            "apparent_temperature": current.get("apparent_temperature"),
            "precipitation": current.get("precipitation"),
            "weather_code": current.get("weather_code"),
            "condition": WMO_CODES.get(current.get("weather_code", 0), "Unknown"),
            "wind_speed_10m": current.get("wind_speed_10m"),
        },
        "forecast_7day": forecast,
        "farming_advisory": advisory,
    }


def _generate_weather_advisory(current: dict, forecast: list) -> list[str]:
    """Generate simple weather-based farming advisories."""
    advisories = []
    temp = current.get("temperature_2m", 25)
    humidity = current.get("relative_humidity_2m", 60)
    rain = current.get("precipitation", 0)

    if temp > 40:
        advisories.append("⚠️ Extreme heat: Irrigate crops in early morning. Provide shade to nurseries.")
    elif temp < 10:
        advisories.append("❄️ Cold wave risk: Cover seedlings; delay sowing if temperature drops further.")

    if humidity > 85:
        advisories.append("🍄 High humidity: High risk of fungal diseases. Monitor crops closely.")

    if rain > 50:
        advisories.append("🌊 Heavy rainfall: Ensure proper field drainage. Avoid spraying pesticides.")
    elif rain == 0:
        rain_next_days = sum(f["precipitation"] for f in forecast[:3])
        if rain_next_days == 0:
            advisories.append("🏜️ No rain in 3-day forecast: Plan irrigation accordingly.")

    # Check for extreme events in forecast
    for f in forecast[:3]:
        if f["precipitation"] > 100:
            advisories.append(f"⛈️ Heavy rain expected on {f['date']}. Protect stored crops.")
            break

    if not advisories:
        advisories.append("✅ Weather conditions are favorable for farming operations.")

    return advisories
