"""
Location Intelligence Agent - Real LangGraph Agent
Rol: Detector de ubicación y contexto espacial
"""

from typing import Dict, Any, List
try:
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_groq import ChatGroq
    from langchain_core.agents import AgentAction, AgentFinish
except Exception:
    # Provide lightweight fallbacks so the module can be imported without langchain packages
    def tool(fn):
        return fn

    class HumanMessage:
        def __init__(self, content: str):
            self.content = content

    class SystemMessage:
        def __init__(self, content: str):
            self.content = content

    ChatGroq = None

    class AgentAction:
        pass

    class AgentFinish:
        pass
import requests
import logging
import os

logger = logging.getLogger(__name__)

# ===== TOOLS PARA EL AGENTE =====

@tool
def get_location_details(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get detailed location information from GPS coordinates using OpenStreetMap Nominatim.

    Args:
        latitude: GPS latitude coordinate
        longitude: GPS longitude coordinate

    Returns:
        Dictionary with location details including address, district, and nearby landmarks
    """
    try:
        # Use Nominatim for reverse geocoding to get address details
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
            "addressdetails": 1,
            "accept-language": "es,en",
            "zoom": 18
        }

        headers = {
            "User-Agent": "RatoncitoPerez/1.0 (Madrid Tourism Guide)"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        logger.info(f"Location lookup successful for ({latitude}, {longitude})")

        if "address" in data:
            address = data["address"]

            # Enhanced location details with better Madrid-specific extraction
            location_info = {
                "coordinates": {"lat": latitude, "lon": longitude},
                "full_address": data.get("display_name", ""),
                "street": address.get("road", address.get("pedestrian", "")),
                "house_number": address.get("house_number", ""),
                "district": address.get("suburb", address.get("neighbourhood", address.get("quarter", ""))),
                "city_district": address.get("city_district", ""),
                "postcode": address.get("postcode", ""),
                "city": address.get("city", address.get("town", "Madrid")),
                "country": address.get("country", "España"),
                "landmark": address.get("tourism", address.get("historic", "")),
                "formatted_address": _format_madrid_address(address),
                "area_description": _get_area_description(address, latitude, longitude),

                # Keep original format for compatibility
                "place_name": data.get("display_name", ""),
                "address": address,
                "place_type": data.get("type", "location"),
                "category": data.get("category", "place"),
                "importance": data.get("importance", 0.5),
                "raw_data": data
            }

            logger.info(f"Location details extracted: {location_info['formatted_address']}")
            return location_info
        else:
            logger.warning("No address details found in geocoding response")
            return _get_fallback_location_info(latitude, longitude)

    except Exception as e:
        logger.error(f"Error getting location details: {e}")
        return _get_fallback_location_info(latitude, longitude)

def _format_madrid_address(address: Dict[str, str]) -> str:
    """Format address in a user-friendly way for Madrid"""
    components = []

    # Add street with house number
    street = address.get("road") or address.get("pedestrian", "")
    if street:
        if address.get("house_number"):
            street += f", {address['house_number']}"
        components.append(street)

    # Add district/neighbourhood (more comprehensive)
    district = (address.get("suburb") or
               address.get("neighbourhood") or
               address.get("quarter") or
               address.get("city_district"))
    if district:
        components.append(district)

    # Add postal code if available
    if address.get("postcode"):
        components.append(address["postcode"])

    # Add city
    city = address.get("city") or address.get("town") or "Madrid"
    components.append(city)

    return ", ".join(components)

def _get_area_description(address: Dict[str, str], lat: float, lon: float) -> str:
    """Get a descriptive area summary for Madrid locations"""
    # Check if we're in a famous Madrid area
    district = address.get("suburb", "").lower()
    neighbourhood = address.get("neighbourhood", "").lower()
    quarter = address.get("quarter", "").lower()

    area_names = [district, neighbourhood, quarter]

    # Famous Madrid areas
    if any("malasaña" in area for area in area_names):
        return "en el trendy barrio de Malasaña, conocido por su ambiente bohemio"
    elif any("chueca" in area for area in area_names):
        return "en Chueca, el corazón cultural LGBTQ+ de Madrid"
    elif any("sol" in area for area in area_names) or any("centro" in area for area in area_names):
        return "en el centro histórico de Madrid, cerca de los principales monumentos"
    elif any("retiro" in area for area in area_names):
        return "en la zona del Retiro, cerca del famoso parque"
    elif any("salamanca" in area for area in area_names):
        return "en el elegante barrio de Salamanca, zona de compras de lujo"
    elif any("lavapiés" in area for area in area_names):
        return "en Lavapiés, el barrio multicultural y artístico"
    elif any("las letras" in area for area in area_names) or any("huertas" in area for area in area_names):
        return "en el Barrio de las Letras, cuna del Siglo de Oro español"
    elif any("chamberí" in area for area in area_names):
        return "en Chamberí, un barrio residencial con encanto"
    else:
        # Generic description based on proximity to center
        if _calculate_distance(lat, lon, 40.4168, -3.7038) < 1:  # Distance to Puerta del Sol
            return "en el centro de Madrid"
        elif _calculate_distance(lat, lon, 40.4168, -3.7038) < 3:
            return "cerca del centro de Madrid"
        else:
            return "en Madrid"

def _get_fallback_location_info(latitude: float, longitude: float) -> Dict[str, Any]:
    """Enhanced fallback location info when geocoding fails"""
    # Try to determine rough area based on coordinates
    area_desc = "Madrid"
    district = "Centro"

    # Basic area detection for Madrid
    if 40.41 <= latitude <= 40.43 and -3.71 <= longitude <= -3.69:
        area_desc = "centro de Madrid"
        district = "Centro"
    elif 40.42 <= latitude <= 40.44 and -3.70 <= longitude <= -3.68:
        area_desc = "zona de Chueca-Malasaña"
        district = "Centro"
    elif 40.40 <= latitude <= 40.42 and -3.70 <= longitude <= -3.68:
        area_desc = "zona del Retiro"
        district = "Retiro"

    return {
        "coordinates": {"lat": latitude, "lon": longitude},
        "full_address": f"Ubicación en {area_desc} ({latitude:.4f}, {longitude:.4f})",
        "street": "",
        "district": district,
        "city": "Madrid",
        "country": "España",
        "formatted_address": f"{area_desc}, Madrid",
        "area_description": f"en {area_desc}",

        # Keep original format for compatibility
        "place_name": f"Ubicación en {area_desc}",
        "address": {"city": "Madrid", "country": "España"},
        "place_type": "location",
        "category": "place",
        "importance": 0.5
    }

@tool
def find_nearby_pois(latitude: float, longitude: float, radius: int = 500) -> List[Dict[str, Any]]:
    """
    Find nearby points of interest using official Madrid tourism data sources.

    Args:
        latitude: GPS latitude coordinate
        longitude: GPS longitude coordinate
        radius: Search radius in meters (default 500m)

    Returns:
        List of nearby POIs with names, types, and distances
    """
    try:
        # Official Madrid tourism and cultural data endpoints
        tourism_endpoints = [
            # Madrid Open Data - Tourist attractions (official)
            "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json",
            # Madrid Open Data - Museums
            "https://datos.madrid.es/egob/catalogo/200761-0-museos.json",
            # Madrid Open Data - Monuments and historic buildings
            "https://datos.madrid.es/egob/catalogo/200304-0-monumentos-edificios-singulares.json",
            # Madrid Open Data - Parks and gardens
            "https://datos.madrid.es/egob/catalogo/200761-0-parques-jardines.json",
            # Madrid Open Data - Cultural centers
            "https://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.json",
            # Madrid Open Data - Tourist information points
            "https://datos.madrid.es/egob/catalogo/200761-0-oficinas-informacion-turistica.json"
        ]

        all_pois = []
        major_attractions_found = []

        # Process each official data source
        for endpoint in tourism_endpoints:
            try:
                logger.info(f"Fetching tourism data from: {endpoint.split('/')[-1]}")
                response = requests.get(endpoint, timeout=15)
                response.raise_for_status()
                data = response.json()

                # Parse Madrid Open Data format
                items = []
                if "@graph" in data:
                    items = data["@graph"]
                elif "data" in data:
                    items = data["data"]
                elif isinstance(data, list):
                    items = data

                for item in items:
                    poi_data = _extract_poi_from_madrid_data(item, latitude, longitude, radius)
                    if poi_data:
                        all_pois.append(poi_data)

                        # Track major attractions
                        if _is_major_attraction(poi_data["name"]):
                            major_attractions_found.append(poi_data)

            except Exception as e:
                logger.warning(f"Error fetching from {endpoint}: {e}")
                continue

        # Add major Madrid landmarks with exact coordinates (highest priority)
        landmark_pois = _get_major_madrid_attractions(latitude, longitude, radius)
        all_pois.extend(landmark_pois)

        # Remove duplicates by name and sort by importance
        unique_pois = _deduplicate_and_prioritize_pois(all_pois)

        # If still no major attractions found, use enhanced Overpass query
        if not any(_is_major_attraction(poi["name"]) for poi in unique_pois):
            logger.info("No major attractions found, using enhanced Overpass query")
            overpass_pois = _enhanced_overpass_query(latitude, longitude, radius)
            unique_pois.extend(overpass_pois)
            unique_pois = _deduplicate_and_prioritize_pois(unique_pois)

        # Final sort: major attractions first, then by distance
        final_pois = sorted(unique_pois, key=lambda x: (
            not _is_major_attraction(x["name"]),  # Major attractions first
            not x.get("is_major", False),         # Flagged major attractions
            x["distance_km"]                      # Then by distance
        ))

        logger.info(f"Found {len(final_pois)} POIs, including major attractions: {[p['name'] for p in final_pois if _is_major_attraction(p['name'])]}")

        return final_pois[:12]  # Return top 12 POIs

    except Exception as e:
        logger.error(f"Error finding nearby POIs: {e}")
        return _get_major_madrid_attractions(latitude, longitude, 2000)  # Fallback with larger radius

def _extract_poi_from_madrid_data(item: Dict, lat: float, lon: float, radius: int) -> Dict[str, Any]:
    """Extract POI data from Madrid Open Data format"""
    try:
        # Extract coordinates (multiple formats in Madrid Open Data)
        poi_lat, poi_lon = None, None

        if "location" in item:
            if isinstance(item["location"], dict):
                poi_lat = float(item["location"].get("latitude", 0))
                poi_lon = float(item["location"].get("longitude", 0))
            elif isinstance(item["location"], str) and "," in item["location"]:
                coords = item["location"].split(",")
                poi_lat, poi_lon = float(coords[0]), float(coords[1])

        elif "geometry" in item and "coordinates" in item["geometry"]:
            coords = item["geometry"]["coordinates"]
            if len(coords) >= 2:
                poi_lon, poi_lat = float(coords[0]), float(coords[1])

        elif "latitud" in item and "longitud" in item:
            poi_lat = float(item["latitud"])
            poi_lon = float(item["longitud"])

        elif "address" in item and "area" in item["address"]:
            # Some Madrid data has area coordinates
            area = item["address"]["area"]
            if "latitude" in area and "longitude" in area:
                poi_lat = float(area["latitude"])
                poi_lon = float(area["longitude"])

        if not poi_lat or not poi_lon:
            return None

        # Calculate distance
        distance = _calculate_distance(lat, lon, poi_lat, poi_lon)
        if distance > radius / 1000:  # Convert radius to km
            return None

        # Extract name (multiple formats)
        name = ""
        if "title" in item:
            name = item["title"]
        elif "nombre" in item:
            name = item["nombre"]
        elif "@id" in item:
            name = item["@id"]
        elif "dc:title" in item:
            name = item["dc:title"]

        if isinstance(name, dict):
            name = name.get("es", name.get("@value", str(name)))

        name = str(name).strip()
        if not name or len(name) < 3:
            return None

        # Determine POI type and importance
        poi_type = "attraction"
        is_major = False

        # Check if it's a major attraction
        if _is_major_attraction(name):
            is_major = True
            poi_type = "major_attraction"
        elif any(word in name.lower() for word in ["museo", "museum"]):
            poi_type = "museum"
        elif any(word in name.lower() for word in ["palacio", "palace", "real"]):
            poi_type = "monument"
            is_major = True
        elif any(word in name.lower() for word in ["plaza", "puerta", "gate"]):
            poi_type = "monument"
        elif any(word in name.lower() for word in ["parque", "park", "jardín", "garden"]):
            poi_type = "park"
        elif any(word in name.lower() for word in ["centro cultural", "teatro", "theatre"]):
            poi_type = "cultural_center"

        return {
            "name": name,
            "type": poi_type,
            "lat": poi_lat,
            "lon": poi_lon,
            "distance_km": round(distance, 2),
            "description": item.get("description", item.get("descripcion", "")),
            "address": item.get("address", item.get("direccion", "")),
            "source": "madrid_open_data",
            "is_major": is_major
        }

    except Exception as e:
        logger.debug(f"Error extracting POI: {e}")
        return None

def _is_major_attraction(name: str) -> bool:
    """Check if a place is a major Madrid tourist attraction"""
    name_lower = name.lower()
    major_keywords = [
        "plaza mayor", "puerta del sol", "palacio real", "prado", "retiro",
        "reina sofía", "thyssen", "cibeles", "gran vía", "templo debod",
        "almudena", "real madrid", "santiago bernabéu", "wanda metropolitano",
        "faro de moncloa", "telefónica", "círculo bellas artes",
        "casa de campo", "madrid río", "mercado san miguel",
        "puerta de alcalá", "plaza españa", "malasaña", "chueca",
        "barrio salamanca", "rastro", "el rastro"
    ]

    return any(keyword in name_lower for keyword in major_keywords)

def _get_major_madrid_attractions(latitude: float, longitude: float, radius: int) -> List[Dict[str, Any]]:
    """Get major Madrid attractions with exact coordinates"""
    major_attractions = [
        # Top tier attractions
        {"name": "Plaza Mayor", "lat": 40.4155, "lon": -3.7074, "type": "major_attraction", "is_major": True},
        {"name": "Palacio Real de Madrid", "lat": 40.4180, "lon": -3.7142, "type": "major_attraction", "is_major": True},
        {"name": "Puerta del Sol", "lat": 40.4168, "lon": -3.7038, "type": "major_attraction", "is_major": True},
        {"name": "Museo del Prado", "lat": 40.4138, "lon": -3.6921, "type": "museum", "is_major": True},
        {"name": "Parque del Retiro", "lat": 40.4152, "lon": -3.6844, "type": "park", "is_major": True},
        {"name": "Museo Reina Sofía", "lat": 40.4077, "lon": -3.6946, "type": "museum", "is_major": True},
        {"name": "Museo Thyssen-Bornemisza", "lat": 40.4165, "lon": -3.6935, "type": "museum", "is_major": True},
        {"name": "Plaza de Cibeles", "lat": 40.4197, "lon": -3.6931, "type": "monument", "is_major": True},
        {"name": "Templo de Debod", "lat": 40.4240, "lon": -3.7177, "type": "monument", "is_major": True},
        {"name": "Gran Vía", "lat": 40.4200, "lon": -3.7014, "type": "major_attraction", "is_major": True},

        # Second tier attractions
        {"name": "Teatro Real", "lat": 40.4180, "lon": -3.7109, "type": "cultural_center", "is_major": False},
        {"name": "Plaza de España", "lat": 40.4238, "lon": -3.7126, "type": "monument", "is_major": False},
        {"name": "Catedral de la Almudena", "lat": 40.4154, "lon": -3.7144, "type": "monument", "is_major": False},
        {"name": "Puerta de Alcalá", "lat": 40.4203, "lon": -3.6895, "type": "monument", "is_major": False},
        {"name": "Círculo de Bellas Artes", "lat": 40.4194, "lon": -3.6978, "type": "cultural_center", "is_major": False},
        {"name": "Mercado de San Miguel", "lat": 40.4152, "lon": -3.7081, "type": "attraction", "is_major": False},
        {"name": "Basílica de San Francisco el Grande", "lat": 40.4097, "lon": -3.7129, "type": "monument", "is_major": False},
        {"name": "Casa de Campo", "lat": 40.4039, "lon": -3.7494, "type": "park", "is_major": False},
        {"name": "Madrid Río", "lat": 40.4000, "lon": -3.7200, "type": "park", "is_major": False},
        {"name": "Faro de Moncloa", "lat": 40.4355, "lon": -3.7170, "type": "attraction", "is_major": False}
    ]

    nearby_attractions = []
    for attraction in major_attractions:
        distance = _calculate_distance(latitude, longitude, attraction["lat"], attraction["lon"])
        if distance <= radius / 1000:  # Convert to km
            attraction_copy = attraction.copy()
            attraction_copy["distance_km"] = round(distance, 2)
            attraction_copy["source"] = "curated_landmarks"
            attraction_copy["description"] = f"Atracción turística principal de Madrid"
            nearby_attractions.append(attraction_copy)

    return nearby_attractions

def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula (returns km)"""
    import math

    R = 6371  # Earth's radius in kilometers

    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (math.sin(dlat/2)**2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))

    return R * c

def _enhanced_overpass_query(latitude: float, longitude: float, radius: int) -> List[Dict[str, Any]]:
    """Enhanced Overpass query focused on major tourist attractions"""
    try:
        overpass_url = "http://overpass-api.de/api/interpreter"

        # Very specific query for major attractions only
        query = f"""
        [out:json][timeout:20];
        (
          node["tourism"="attraction"]["name"~"Plaza|Palacio|Puerta|Museo|Prado|Reina|Thyssen"](around:{radius},{latitude},{longitude});
          node["historic"="monument"]["name"~"Plaza|Palacio|Puerta|Cibeles|Alcalá"](around:{radius},{latitude},{longitude});
          node["amenity"="theatre"]["name"~"Real|Teatro"](around:{radius},{latitude},{longitude});
          node["leisure"="park"]["name"~"Retiro|Casa de Campo"](around:{radius},{latitude},{longitude});
          way["tourism"="attraction"]["name"~"Plaza|Palacio|Gran Vía"](around:{radius},{latitude},{longitude});
          way["historic"="monument"]["name"~"Plaza|Palacio"](around:{radius},{latitude},{longitude});
        );
        out center;
        """

        response = requests.post(overpass_url, data=query, timeout=20)
        response.raise_for_status()
        data = response.json()

        pois = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name", "").strip()

            if not name or len(name) < 5:
                continue

            # Get coordinates
            if "center" in element:
                poi_lat, poi_lon = element["center"]["lat"], element["center"]["lon"]
            else:
                poi_lat, poi_lon = element.get("lat"), element.get("lon")

            if poi_lat and poi_lon:
                distance = _calculate_distance(latitude, longitude, poi_lat, poi_lon)

                poi_type = "attraction"
                is_major = _is_major_attraction(name)

                if tags.get("tourism") == "museum" or "museo" in name.lower():
                    poi_type = "museum"
                elif tags.get("historic") == "monument":
                    poi_type = "monument"
                elif tags.get("leisure") == "park":
                    poi_type = "park"
                elif tags.get("amenity") == "theatre":
                    poi_type = "cultural_center"

                pois.append({
                    "name": name,
                    "type": poi_type,
                    "lat": poi_lat,
                    "lon": poi_lon,
                    "distance_km": round(distance, 2),
                    "description": tags.get("description", ""),
                    "source": "openstreetmap_enhanced",
                    "is_major": is_major
                })

        return pois

    except Exception as e:
        logger.error(f"Enhanced Overpass query failed: {e}")
        return []

def _deduplicate_and_prioritize_pois(pois: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicates and prioritize by importance"""
    seen_names = set()
    unique_pois = []

    # Sort by priority: major attractions first, then by distance
    sorted_pois = sorted(pois, key=lambda x: (
        not x.get("is_major", False),
        not _is_major_attraction(x["name"]),
        x["distance_km"]
    ))

    for poi in sorted_pois:
        name_normalized = poi["name"].lower().strip()

        # Skip if we've seen a very similar name
        if not any(name_normalized in seen or seen in name_normalized for seen in seen_names):
            seen_names.add(name_normalized)
            unique_pois.append(poi)

            # Limit total results
            if len(unique_pois) >= 15:
                break

    return unique_pois

@tool
def calculate_distance_to_landmarks(latitude: float, longitude: float) -> Dict[str, float]:
    """
    Calculate distances to major Madrid landmarks.

    Args:
        latitude: Current GPS latitude
        longitude: Current GPS longitude

    Returns:
        Dictionary with landmark names and distances in kilometers
    """
    import math

    # Major Madrid landmarks coordinates
    landmarks = {
        "Plaza Mayor": (40.4150, -3.7037),
        "Palacio Real": (40.4180, -3.7142),
        "Puerta del Sol": (40.4168, -3.7038),
        "Parque del Retiro": (40.4152, -3.6844),
        "Museo del Prado": (40.4138, -3.6921),
        "Plaza de Cibeles": (40.4197, -3.6931),
        "Templo de Debod": (40.4240, -3.7177),
        "Gran Vía": (40.4200, -3.7014)
    }

    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers

        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = (math.sin(dlat/2)**2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    distances = {}
    for landmark, (lm_lat, lm_lon) in landmarks.items():
        distance = haversine_distance(latitude, longitude, lm_lat, lm_lon)
        distances[landmark] = round(distance, 2)

    return distances

# ===== AGENTE LOCATION INTELLIGENCE =====

class LocationIntelligenceAgent:
    """
    Real LangGraph Agent for Location Intelligence
    Uses tools to analyze GPS coordinates and provide contextual location information
    """

    def __init__(self):
        self.llm = self._initialize_llm()
        self.tools = [get_location_details, find_nearby_pois, calculate_distance_to_landmarks]

    def _initialize_llm(self):
        """Initialize Groq LLM for the agent"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None

        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=800
        )

    def analyze_location(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Main method to analyze a location using agent tools

        Args:
            latitude: GPS latitude coordinate
            longitude: GPS longitude coordinate

        Returns:
            Dictionary with comprehensive location analysis
        """
        try:
            # Step 1: Get basic location details
            location_details = get_location_details.invoke({"latitude": latitude, "longitude": longitude})

            # Step 2: Find nearby points of interest
            nearby_pois = find_nearby_pois.invoke({"latitude": latitude, "longitude": longitude, "radius": 500})

            # Step 3: Calculate distances to landmarks
            landmark_distances = calculate_distance_to_landmarks.invoke({"latitude": latitude, "longitude": longitude})

            # Step 4: Use LLM to synthesize information
            analysis = self._synthesize_location_analysis(
                location_details, nearby_pois, landmark_distances, latitude, longitude
            )

            return {
                "location_details": location_details,
                "nearby_pois": nearby_pois,
                "landmark_distances": landmark_distances,
                "analysis": analysis,
                "coordinates": {"latitude": latitude, "longitude": longitude}
            }

        except Exception as e:
            logger.error(f"Error in location analysis: {e}")
            return {
                "location_details": {"place_name": "Madrid Centro", "error": str(e)},
                "nearby_pois": [],
                "landmark_distances": {},
                "analysis": "Error analyzing location",
                "coordinates": {"latitude": latitude, "longitude": longitude}
            }

    def _synthesize_location_analysis(self, location_details: Dict, pois: List[Dict],
                                    landmarks: Dict, lat: float, lon: float) -> str:
        """
        Use LLM to create intelligent analysis of location context
        """
        try:
            system_prompt = """
Eres un experto analista de ubicaciones de Madrid especializado en turismo familiar.
Analiza la información de ubicación proporcionada y crea un resumen contextual preciso y útil.

IMPORTANTE:
- USA SOLO información real y verificable
- NO inventes lugares que no existen
- Si hay pocos datos, menciona solo lo que está confirmado
- Prioriza monumentos y sitios culturales sobre restaurantes

Tu respuesta debe incluir:
1. Descripción precisa del lugar actual
2. Tipo de zona (histórica, comercial, residencial, turística)
3. Puntos de interés culturales/turísticos cercanos REALES
4. Contexto histórico si es relevante
5. Accesibilidad para familias con niños

Mantén el tono informativo pero amigable. Máximo 150 palabras.
"""

            # Format POIs by type for better context
            museums = [poi for poi in pois if poi["type"] == "museum"]
            monuments = [poi for poi in pois if poi["type"] == "monument"]
            parks = [poi for poi in pois if poi["type"] == "park"]
            cultural = [poi for poi in pois if poi["type"] == "cultural_center"]

            user_prompt = f"""
UBICACIÓN ACTUAL:
- Lugar: {location_details.get('place_name', 'Madrid')}
- Tipo: {location_details.get('place_type', 'lugar')}
- Coordenadas: {lat:.4f}, {lon:.4f}

PUNTOS DE INTERÉS CULTURALES CERCANOS:
Museos: {[m['name'] for m in museums[:3]]}
Monumentos: {[m['name'] for m in monuments[:3]]}
Parques: {[p['name'] for p in parks[:2]]}
Centros culturales: {[c['name'] for c in cultural[:2]]}

MONUMENTOS PRINCIPALES DE MADRID (distancias):
{', '.join([f"{name}: {dist}km" for name, dist in list(landmarks.items())[:4]])}

DATOS VERIFICADOS: Los puntos de interés provienen de {pois[0].get('source', 'fuentes oficiales') if pois else 'datos oficiales de Madrid'}.

Proporciona un análisis contextual preciso y útil de esta ubicación, enfocándote en patrimonio cultural y turismo familiar.
"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = self.llm.invoke(messages)
            return response.content

        except Exception as e:
            logger.error(f"Error in LLM synthesis: {e}")
            place_name = location_details.get('place_name', 'Madrid Centro')

            # Create a basic but accurate fallback
            cultural_pois = [poi['name'] for poi in pois if poi['type'] in ['museum', 'monument', 'cultural_center']][:3]
            if cultural_pois:
                return f"Te encuentras en {place_name}. Cerca tienes sitios de interés cultural como {', '.join(cultural_pois)}. Esta zona forma parte del rico patrimonio histórico de Madrid."
            else:
                return f"Te encuentras en {place_name}, una zona de Madrid con historia y encanto por descubrir."

# Global instance
location_agent = LocationIntelligenceAgent()
