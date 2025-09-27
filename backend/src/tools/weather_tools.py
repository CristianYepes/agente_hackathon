import requests
import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_weather_context(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """
    Get current weather and basic forecast for Madrid location
    Uses OpenWeatherMap free tier (1000 calls/day)
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        logger.warning("No OpenWeatherMap API key found, using mock weather data")
        return get_mock_weather()
    
    try:
        # Current weather
        current_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
            "lang": "es"
        }
        
        response = requests.get(current_url, params=params, timeout=10)
        response.raise_for_status()
        
        weather_data = response.json()
        
        return {
            "temperature": round(weather_data["main"]["temp"]),
            "feels_like": round(weather_data["main"]["feels_like"]),
            "condition": weather_data["weather"][0]["description"],
            "main_condition": weather_data["weather"][0]["main"].lower(),
            "humidity": weather_data["main"]["humidity"],
            "wind_speed": weather_data.get("wind", {}).get("speed", 0),
            "clouds": weather_data["clouds"]["all"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return get_mock_weather()

def get_mock_weather() -> Dict[str, Any]:
    """
    Provide mock weather data when API is unavailable
    """
    return {
        "temperature": 20,
        "feels_like": 18,
        "condition": "parcialmente nublado",
        "main_condition": "clouds",
        "humidity": 65,
        "wind_speed": 2.5,
        "clouds": 40,
        "timestamp": datetime.now().isoformat(),
        "mock": True
    }

def get_time_context() -> Dict[str, Any]:
    """
    Get current time context for activity suggestions
    """
    now = datetime.now()
    hour = now.hour
    
    # Determine time period
    if 6 <= hour < 12:
        period = "morning"
        period_es = "mañana"
    elif 12 <= hour < 17:
        period = "afternoon"
        period_es = "tarde"
    elif 17 <= hour < 21:
        period = "evening"
        period_es = "atardecer"
    else:
        period = "night"
        period_es = "noche"
    
    return {
        "hour": hour,
        "period": period,
        "period_es": period_es,
        "is_weekend": now.weekday() >= 5,
        "day_of_week": now.strftime("%A"),
        "date": now.strftime("%Y-%m-%d"),
        "season": get_season()
    }

def get_season() -> str:
    """
    Get current season in Spain
    """
    month = datetime.now().month
    
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"

def should_suggest_indoor_activities(weather: Dict[str, Any]) -> bool:
    """
    Determine if indoor activities should be prioritized based on weather
    """
    if weather.get("mock"):
        return False
    
    # Rain conditions
    if weather["main_condition"] in ["rain", "thunderstorm", "drizzle"]:
        return True
    
    # Extreme temperatures
    if weather["temperature"] < 5 or weather["temperature"] > 35:
        return True
    
    # Strong wind
    if weather["wind_speed"] > 10:
        return True
    
    return False

def get_activity_weather_context(weather: Dict[str, Any], time: Dict[str, Any]) -> str:
    """
    Generate weather-appropriate activity context for the Ratoncito
    """
    temp = weather["temperature"]
    condition = weather["condition"]
    period = time["period_es"]
    
    if should_suggest_indoor_activities(weather):
        return f"Con este tiempo de {condition} y {temp}°C, mejor busquemos aventuras bajo techo en esta {period}."
    elif temp > 25:
        return f"¡Qué {period} tan soleada! Con {temp}°C, perfecto para jugar a la sombra."
    elif temp < 10:
        return f"¡Brr! Con {temp}°C necesitamos actividades que nos den calorcito en esta {period}."
    else:
        return f"¡Perfecto! Con {temp}°C y {condition}, ideal para explorar Madrid en esta {period}."
