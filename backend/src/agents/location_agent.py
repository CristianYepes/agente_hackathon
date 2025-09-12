import os
import logging
from typing import Dict, Any
from langchain_groq import ChatGroq
from src.tools.location_tools import get_location_context, get_nearby_attractions

logger = logging.getLogger(__name__)

class LocationIntelligenceAgent:
    def __init__(self):
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("No GROQ_API_KEY found, using mock responses")
            return None

        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=500
        )

    def analyze_location(self, latitude: float, longitude: float) -> Dict[str, Any]:
        try:
            logger.info(f"🌍 Analyzing location: {latitude}, {longitude}")

            location_context = get_location_context(latitude, longitude)
            nearby_attractions = get_nearby_attractions(latitude, longitude)

            if self.llm:
                enhanced_analysis = self._enhance_with_llm(location_context, nearby_attractions)
            else:
                enhanced_analysis = self._create_mock_analysis(location_context)

            result = {
                "location_details": location_context,
                "nearby_attractions": nearby_attractions,
                "analysis": enhanced_analysis,
                "family_friendly_score": self._calculate_family_score(location_context),
                "recommended_activities": self._get_location_activities(location_context)
            }

            logger.info(f"✅ Location analysis completed for {location_context.get('place_name', 'Unknown')}")
            return result

        except Exception as e:
            logger.error(f"❌ Error in location analysis: {e}")
            return self._create_fallback_analysis(latitude, longitude)

    def _enhance_with_llm(self, location_context: Dict[str, Any], nearby_attractions: list) -> str:
        try:
            place_name = location_context.get("place_name", "Madrid")
            place_type = location_context.get("place_type", "general")
            significance = location_context.get("significance", "Una ubicación especial")

            attractions_text = ", ".join([attr.get("name", "") for attr in nearby_attractions[:3]])

            prompt = f"""Como experto en Madrid y guía turístico familiar, analiza esta ubicación:

Lugar: {place_name}
Tipo: {place_type}
Significado: {significance}
Atracciones cercanas: {attractions_text}

Proporciona un análisis breve (máximo 100 palabras) sobre:
1. Por qué es especial este lugar
2. Qué lo hace interesante para familias
3. Contexto histórico o cultural relevante

Responde de forma educativa pero accesible para familias con niños."""

            response = self.llm.invoke(prompt)
            return response.content

        except Exception as e:
            logger.error(f"Error enhancing with LLM: {e}")
            return self._create_mock_analysis(location_context)

    def _create_mock_analysis(self, location_context: Dict[str, Any]) -> str:
        place_name = location_context.get("place_name", "Madrid")
        significance = location_context.get("significance", "Una ubicación especial en Madrid")

        return f"""{place_name} es un lugar fascinante en Madrid. {significance}

Este lugar tiene una rica historia que se remonta a siglos pasados. Es perfecto para familias que quieren explorar Madrid, ya que ofrece una combinación única de historia, cultura y entretenimiento.

Los niños pueden aprender sobre la historia de Madrid mientras disfrutan de la arquitectura y el ambiente especial de este lugar."""

    def _calculate_family_score(self, location_context: Dict[str, Any]) -> float:
        score = 0.5

        place_type = location_context.get("place_type", "")
        if place_type in ["park", "plaza", "tourist_attraction"]:
            score += 0.3
        elif place_type in ["museum", "palace"]:
            score += 0.2

        if location_context.get("is_tourist_area", False):
            score += 0.2

        nearby_attractions = location_context.get("nearby_attractions", [])
        if len(nearby_attractions) > 2:
            score += 0.1

        return min(score, 1.0)

    def _get_location_activities(self, location_context: Dict[str, Any]) -> list:
        place_type = location_context.get("place_type", "general")
        place_name = location_context.get("place_name", "este lugar")

        activities_map = {
            "plaza": [
                f"Explorar la arquitectura de {place_name}",
                "Buscar detalles decorativos únicos",
                "Contar ventanas y balcones",
                "Imaginar la vida en épocas pasadas"
            ],
            "park": [
                f"Pasear por los senderos de {place_name}",
                "Observar plantas y animales",
                "Buscar fuentes y estatuas",
                "Hacer un picnic familiar"
            ],
            "palace": [
                f"Admirar la fachada de {place_name}",
                "Contar columnas y ventanas",
                "Buscar escudos reales",
                "Fotografiar detalles arquitectónicos"
            ],
            "museum": [
                f"Planificar una visita a {place_name}",
                "Buscar información sobre exposiciones",
                "Preparar preguntas para la visita",
                "Explorar el área exterior"
            ]
        }

        return activities_map.get(place_type, [
            f"Explorar {place_name}",
            "Buscar detalles interesantes",
            "Tomar fotografías familiares",
            "Aprender sobre la historia del lugar"
        ])

    def _create_fallback_analysis(self, latitude: float, longitude: float) -> Dict[str, Any]:
        return {
            "location_details": {
                "place_name": "Madrid Centro",
                "place_type": "historical_center",
                "significance": "Corazón histórico de Madrid",
                "coordinates": {"lat": latitude, "lon": longitude},
                "is_tourist_area": True
            },
            "nearby_attractions": [
                {"name": "Plaza Mayor", "type": "attraction", "distance": 200},
                {"name": "Puerta del Sol", "type": "attraction", "distance": 300}
            ],
            "analysis": "Estás en una zona histórica de Madrid, perfecta para explorar en familia.",
            "family_friendly_score": 0.8,
            "recommended_activities": [
                "Explorar el centro histórico",
                "Buscar detalles arquitectónicos",
                "Disfrutar del ambiente madrileño"
            ]
        }

location_agent = LocationIntelligenceAgent()
