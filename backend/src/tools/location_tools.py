import requests
import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

def get_location_context(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get location context using reverse geocoding
    """
    try:
        location_data = reverse_geocode(latitude, longitude)

        if location_data:
            return {
                "place_name": location_data.get("display_name", "Madrid"),
                "address": location_data.get("address", {}),
                "place_type": _determine_place_type(location_data),
                "significance": _get_place_significance(location_data),
                "nearby_attractions": get_nearby_attractions(latitude, longitude),
                "coordinates": {"lat": latitude, "lon": longitude},
                "is_tourist_area": _is_tourist_area(location_data)
            }
        else:
            return _get_default_madrid_context(latitude, longitude)

    except Exception as e:
        logger.error(f"Error getting location context: {e}")
        return _get_default_madrid_context(latitude, longitude)

def reverse_geocode(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Reverse geocode coordinates to get location information
    """
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
            "addressdetails": 1,
            "accept-language": "es"
        }

        headers = {
            "User-Agent": "RatoncitoPerez/1.0"
        }

        response = requests.get(url, params=params, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Successfully geocoded {latitude}, {longitude}")
            return data
        else:
            logger.warning(f"Geocoding API returned status {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Error in reverse geocoding: {e}")
        return None

def _determine_place_type(location_data: Dict[str, Any]) -> str:
    """
    Determine the type of place based on geocoding data
    """
    address = location_data.get("address", {})
    place_type = location_data.get("type", "")

    if "tourism" in location_data.get("class", ""):
        return "tourist_attraction"
    elif address.get("amenity") in ["restaurant", "cafe", "bar"]:
        return "dining"
    elif "park" in place_type.lower() or "garden" in place_type.lower():
        return "park"
    elif "museum" in place_type.lower():
        return "museum"
    elif "palace" in place_type.lower() or "castle" in place_type.lower():
        return "palace"
    elif address.get("highway"):
        return "street"
    elif "square" in place_type.lower() or "plaza" in place_type.lower():
        return "plaza"
    else:
        return "general"

def _get_place_significance(location_data: Dict[str, Any]) -> str:
    """
    Get significance description of the place
    """
    place_name = location_data.get("display_name", "").lower()
    address = location_data.get("address", {})

    if "plaza mayor" in place_name:
        return "El corazón histórico de Madrid, construida en el siglo XVII"
    elif "palacio real" in place_name:
        return "La residencia oficial de la familia real española"
    elif "retiro" in place_name:
        return "El parque más famoso de Madrid, perfecto para familias"
    elif "puerta del sol" in place_name:
        return "El kilómetro cero de España y centro neurálgico de Madrid"
    elif "cibeles" in place_name:
        return "Icónico símbolo de Madrid con su famosa fuente"
    elif "prado" in place_name:
        return "Zona de museos de renombre mundial"
    elif address.get("neighbourhood"):
        return f"Barrio de {address['neighbourhood']} en Madrid"
    else:
        return "Una ubicación especial en el corazón de Madrid"

def get_nearby_attractions(latitude: float, longitude: float, radius: int = 1000) -> List[Dict[str, Any]]:
    """
    Get nearby attractions using Overpass API
    """
    try:
        overpass_url = "http://overpass-api.de/api/interpreter"

        query = f"""
        [out:json][timeout:10];
        (
          node["tourism"~"attraction|museum|castle|palace"]["name"](around:{radius},{latitude},{longitude});
          way["tourism"~"attraction|museum|castle|palace"]["name"](around:{radius},{latitude},{longitude});
          relation["tourism"~"attraction|museum|castle|palace"]["name"](around:{radius},{latitude},{longitude});
        );
        out center;
        """

        response = requests.post(overpass_url, data=query, timeout=10)

        if response.status_code == 200:
            data = response.json()
            attractions = []

            for element in data.get("elements", [])[:5]:  # Limit to 5 attractions
                if "name" in element.get("tags", {}):
                    attraction = {
                        "name": element["tags"]["name"],
                        "type": element["tags"].get("tourism", "attraction"),
                        "distance": _calculate_distance(
                            latitude, longitude,
                            element.get("lat", element.get("center", {}).get("lat", 0)),
                            element.get("lon", element.get("center", {}).get("lon", 0))
                        )
                    }
                    attractions.append(attraction)

            attractions.sort(key=lambda x: x["distance"])
            return attractions
        else:
            return _get_default_attractions()

    except Exception as e:
        logger.error(f"Error getting nearby attractions: {e}")
        return _get_default_attractions()

def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate approximate distance between two points in meters
    """
    import math

    R = 6371000  # Earth's radius in meters

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) * math.sin(delta_lon / 2))

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def _is_tourist_area(location_data: Dict[str, Any]) -> bool:
    """
    Determine if location is in a tourist area
    """
    place_name = location_data.get("display_name", "").lower()
    address = location_data.get("address", {})

    tourist_keywords = [
        "plaza mayor", "palacio real", "retiro", "prado", "puerta del sol",
        "cibeles", "gran vía", "malasaña", "chueca", "centro"
    ]

    for keyword in tourist_keywords:
        if keyword in place_name:
            return True

    return address.get("city_district", "").lower() == "centro"

def _get_default_madrid_context(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Return default Madrid context when geocoding fails
    """
    return {
        "place_name": "Madrid Centro",
        "address": {
            "city": "Madrid",
            "country": "España"
        },
        "place_type": "historical_center",
        "significance": "El corazón histórico de Madrid",
        "nearby_attractions": _get_default_attractions(),
        "coordinates": {"lat": latitude, "lon": longitude},
        "is_tourist_area": True
    }

def _get_default_attractions() -> List[Dict[str, Any]]:
    """
    Return default Madrid attractions
    """
    return [
        {
            "name": "Plaza Mayor",
            "type": "attraction",
            "distance": 200
        },
        {
            "name": "Puerta del Sol",
            "type": "attraction",
            "distance": 300
        },
        {
            "name": "Palacio Real",
            "type": "palace",
            "distance": 500
        },
        {
            "name": "Parque del Retiro",
            "type": "park",
            "distance": 800
        },
        {
            "name": "Museo del Prado",
            "type": "museum",
            "distance": 1000
        }
    ]

def get_madrid_districts() -> List[Dict[str, Any]]:
    """
    Get list of Madrid districts with family-friendly information
    """
    return [
        {
            "name": "Centro",
            "description": "Corazón histórico de Madrid",
            "family_friendly": True,
            "main_attractions": ["Plaza Mayor", "Puerta del Sol", "Palacio Real"]
        },
        {
            "name": "Retiro",
            "description": "Zona del famoso parque",
            "family_friendly": True,
            "main_attractions": ["Parque del Retiro", "Museo del Prado"]
        },
        {
            "name": "Salamanca",
            "description": "Distrito elegante de Madrid",
            "family_friendly": True,
            "main_attractions": ["Parque de El Retiro", "Mercado de la Paz"]
        },
        {
            "name": "Arganzuela",
            "description": "Zona moderna junto al río",
            "family_friendly": True,
            "main_attractions": ["Madrid Río", "Matadero Madrid"]
        }
    ]

def is_madrid_coordinates(latitude: float, longitude: float) -> bool:
    """
    Check if coordinates are within Madrid boundaries
    """
    madrid_bounds = {
        "north": 40.5,
        "south": 40.3,
        "east": -3.5,
        "west": -3.9
    }

    return (
        madrid_bounds["south"] <= latitude <= madrid_bounds["north"] and
        madrid_bounds["west"] <= longitude <= madrid_bounds["east"]
    )
