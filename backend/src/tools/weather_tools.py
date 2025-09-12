import requests
import os
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

def get_weather_context(latitude: float, longitude: float) -> Dict[str, Any]:
	"""
	Get weather information for the given coordinates
	"""
	try:
		api_key = os.getenv("OPENWEATHER_API_KEY")

		if not api_key:
			logger.warning("No OpenWeather API key found, using mock data")
			return _get_mock_weather()

		url = f"http://api.openweathermap.org/data/2.5/weather"
		params = {
			"lat": latitude,
			"lon": longitude,
			"appid": api_key,
			"units": "metric",
			"lang": "es"
		}

		response = requests.get(url, params=params, timeout=5)

		if response.status_code == 200:
			data = response.json()

			weather_context = {
				"temperature": f"{round(data['main']['temp'])}°C",
				"description": data['weather'][0]['description'],
				"humidity": f"{data['main']['humidity']}%",
				"wind_speed": f"{data['wind']['speed']} m/s",
				"feels_like": f"{round(data['main']['feels_like'])}°C",
				"outdoor_suitable": _is_outdoor_suitable(data),
				"recommendations": _get_weather_recommendations(data)
			}

			logger.info(f"Weather data retrieved successfully for {latitude}, {longitude}")
			return weather_context

		else:
			logger.warning(f"Weather API returned status {response.status_code}")
			return _get_mock_weather()

	except Exception as e:
		logger.error(f"Error getting weather data: {e}")
		return _get_mock_weather()

def _get_mock_weather() -> Dict[str, Any]:
	"""
	Return mock weather data when API is not available
	"""
	return {
		"temperature": "22°C",
		"description": "soleado",
		"humidity": "65%",
		"wind_speed": "5 m/s",
		"feels_like": "24°C",
		"outdoor_suitable": True,
		"recommendations": [
			"Perfecto para caminar por Madrid",
			"Ideal para visitar parques y plazas",
			"No olvides protección solar"
		]
	}

def _is_outdoor_suitable(weather_data: Dict) -> bool:
	"""
	Determine if weather is suitable for outdoor activities
	"""
	temp = weather_data['main']['temp']
	weather_id = weather_data['weather'][0]['id']

	# Temperature check (5-35°C is comfortable)
	temp_ok = 5 <= temp <= 35

	# Weather condition check (avoid heavy rain, storms, etc.)
	weather_ok = weather_id < 600 or weather_id >= 800

	return temp_ok and weather_ok

def _get_weather_recommendations(weather_data: Dict) -> list:
	"""
	Generate weather-based recommendations
	"""
	temp = weather_data['main']['temp']
	weather_id = weather_data['weather'][0]['id']

	recommendations = []

	if temp < 10:
		recommendations.append("Llevar ropa de abrigo")
		recommendations.append("Considerar actividades en interiores")
	elif temp > 25:
		recommendations.append("Usar protección solar")
		recommendations.append("Llevar agua")
		recommendations.append("Buscar sombra en las plazas")
	else:
		recommendations.append("Temperatura perfecta para caminar")
		recommendations.append("Ideal para actividades al aire libre")

	if weather_id >= 200 and weather_id < 300:  # Thunderstorm
		recommendations.append("Considerar visitas a museos")
		recommendations.append("Actividades cubiertas recomendadas")
	elif weather_id >= 300 and weather_id < 600:  # Drizzle/Rain
		recommendations.append("Llevar paraguas")
		recommendations.append("Visitar galerías cubiertas")
	elif weather_id >= 800:  # Clear/Clouds
		recommendations.append("Perfecto para explorar Madrid")
		recommendations.append("Visitar parques y monumentos")

	return recommendations

def get_time_context() -> Dict[str, Any]:
	"""
	Get current time context and recommendations
	"""
	try:
		now = datetime.now()
		hour = now.hour

		if 6 <= hour < 12:
			time_period = "mañana"
			activities = [
				"Visitar mercados matutinos",
				"Pasear por parques tranquilos",
				"Explorar centros históricos"
			]
			opening_status = "La mayoría de lugares están abriendo"
		elif 12 <= hour < 18:
			time_period = "tarde"
			activities = [
				"Almorzar en terrazas",
				"Visitar museos y monumentos",
				"Explorar plazas principales"
			]
			opening_status = "Todos los lugares están abiertos"
		elif 18 <= hour < 22:
			time_period = "atardecer"
			activities = [
				"Disfrutar del atardecer en miradores",
				"Pasear por el centro iluminado",
				"Cenar en familia"
			]
			opening_status = "Muchos lugares siguen abiertos"
		else:
			time_period = "noche"
			activities = [
				"Paseos nocturnos seguros",
				"Ver la iluminación nocturna",
				"Descansar en hoteles"
			]
			opening_status = "Lugares nocturnos disponibles"

		return {
			"current_time": now.strftime("%H:%M"),
			"time_period": time_period,
			"day_of_week": _get_day_name(now.weekday()),
			"recommended_activities": activities,
			"opening_status": opening_status,
			"is_weekend": now.weekday() >= 5,
			"season": _get_season(now.month)
		}

	except Exception as e:
		logger.error(f"Error getting time context: {e}")
		return {
			"current_time": "12:00",
			"time_period": "día",
			"day_of_week": "día de la semana",
			"recommended_activities": ["Explorar Madrid"],
			"opening_status": "Lugares disponibles",
			"is_weekend": False,
			"season": "primavera"
		}

def _get_day_name(weekday: int) -> str:
	"""
	Convert weekday number to Spanish day name
	"""
	days = [
		"lunes", "martes", "miércoles", "jueves",
		"viernes", "sábado", "domingo"
	]
	return days[weekday]

def _get_season(month: int) -> str:
	"""
	Get season based on month
	"""
	if month in [12, 1, 2]:
		return "invierno"
	elif month in [3, 4, 5]:
		return "primavera"
	elif month in [6, 7, 8]:
		return "verano"
	else:
		return "otoño"

def get_combined_context(latitude: float, longitude: float) -> Dict[str, Any]:
	"""
	Get combined weather and time context
	"""
	try:
		weather = get_weather_context(latitude, longitude)
		time_info = get_time_context()

		combined_recommendations = []
		combined_recommendations.extend(weather.get("recommendations", []))
		combined_recommendations.extend(time_info.get("recommended_activities", []))

		return {
			"weather": weather,
			"time": time_info,
			"combined_recommendations": combined_recommendations,
			"optimal_for_families": weather.get("outdoor_suitable", True) and 6 <= datetime.now().hour <= 20
		}

	except Exception as e:
		logger.error(f"Error getting combined context: {e}")
		return {
			"weather": _get_mock_weather(),
			"time": get_time_context(),
			"combined_recommendations": ["Explorar Madrid en familia"],
			"optimal_for_families": True
		}
