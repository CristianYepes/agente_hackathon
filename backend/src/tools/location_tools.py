import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def reverse_geocode_nominatim(lat: float, lon: float) -> Optional[str]:
    """
    Convert GPS coordinates to Madrid place name using OpenStreetMap Nominatim
    Free and unlimited geocoding service
    """
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1,
            "extratags": 1,
            "namedetails": 1,
            "zoom": 18,
            "accept-language": "es,en"
        }
        
        headers = {
            "User-Agent": "RatoncitoPerezApp/1.0"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract meaningful place name
        if "address" in data:
            address = data["address"]
            
            # Priority order for Madrid landmarks
            place_candidates = [
                address.get("tourism"),
                address.get("amenity"),
                address.get("historic"),
                address.get("leisure"),
                address.get("building"),
                address.get("road"),
                address.get("pedestrian"),
                address.get("neighbourhood"),
                address.get("suburb"),
                address.get("city_district")
            ]
            
            # Find first non-null place name
            for candidate in place_candidates:
                if candidate:
                    return candidate
                    
            # Fallback to display name
            return data.get("display_name", "Madrid Centro").split(",")[0]
            
    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        return None

def detect_madrid_landmark(place_name: str) -> str:
    """
    Enhance detected place with known Madrid landmarks
    """
    madrid_landmarks = {
        "plaza mayor": "Plaza Mayor",
        "mayor": "Plaza Mayor", 
        "palacio real": "Palacio Real de Madrid",
        "palacio": "Palacio Real de Madrid",
        "real": "Palacio Real de Madrid",
        "retiro": "Parque del Retiro",
        "buen retiro": "Parque del Retiro",
        "sol": "Puerta del Sol",
        "puerta del sol": "Puerta del Sol",
        "cibeles": "Plaza de Cibeles",
        "plaza de cibeles": "Plaza de Cibeles",
        "gran vía": "Gran Vía",
        "gran via": "Gran Vía",
        "templo debod": "Templo de Debod",
        "debod": "Templo de Debod",
        "museo del prado": "Museo del Prado",
        "prado": "Museo del Prado",
        "reina sofía": "Museo Reina Sofía",
        "reina sofia": "Museo Reina Sofía",
        "thyssen": "Museo Thyssen-Bornemisza",
        "almudena": "Catedral de la Almudena",
        "catedral": "Catedral de la Almudena"
    }
    
    if not place_name:
        return "Madrid Centro"
        
    place_lower = place_name.lower()
    
    # Check for landmarks in the detected name
    for key, landmark in madrid_landmarks.items():
        if key in place_lower:
            return landmark
            
    return place_name

def get_location_context(lat: float, lon: float) -> Dict[str, Any]:
    """
    Get comprehensive location context including place name and type
    """
    place_name = reverse_geocode_nominatim(lat, lon)
    enhanced_place = detect_madrid_landmark(place_name) if place_name else "Madrid Centro"
    
    # Determine location type for context
    location_type = categorize_location(enhanced_place)
    
    return {
        "place_name": enhanced_place,
        "raw_place": place_name,
        "location_type": location_type,
        "coordinates": {"lat": lat, "lon": lon}
    }

def categorize_location(place_name: str) -> str:
    """
    Categorize location type for appropriate content adaptation
    """
    place_lower = place_name.lower()
    
    if any(word in place_lower for word in ["plaza", "square"]):
        return "plaza"
    elif any(word in place_lower for word in ["palacio", "palace", "real"]):
        return "palace"
    elif any(word in place_lower for word in ["parque", "park", "retiro"]):
        return "park"
    elif any(word in place_lower for word in ["museo", "museum"]):
        return "museum"
    elif any(word in place_lower for word in ["catedral", "cathedral", "iglesia", "church", "templo", "temple"]):
        return "religious"
    elif any(word in place_lower for word in ["calle", "street", "via", "road"]):
        return "street"
    else:
        return "landmark"
