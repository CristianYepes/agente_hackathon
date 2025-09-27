"""
Context Retrieval Agent - Real LangGraph Agent
Rol: Investigador histórico y cultural
"""

from typing import Dict, Any, List
try:
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_groq import ChatGroq
except Exception:
    def tool(fn):
        return fn

    class HumanMessage:
        def __init__(self, content: str):
            self.content = content

    class SystemMessage:
        def __init__(self, content: str):
            self.content = content

    ChatGroq = None
import requests
import logging
import os
import json

logger = logging.getLogger(__name__)

# ===== TOOLS PARA EL AGENTE =====

@tool
def search_madrid_history(location_name: str, location_type: str) -> Dict[str, Any]:
    """
    Search for historical and cultural information about Madrid locations.
    
    Args:
        location_name: Name of the location
        location_type: Type of location (plaza, museum, etc.)
        
    Returns:
        Dictionary with historical information and interesting facts
    """
    try:
        # Search Wikipedia for historical information
        wikipedia_info = _search_wikipedia(location_name)
        
        # Search Madrid Open Data for cultural events and info
        cultural_info = _search_madrid_cultural_data(location_name)
        
        # Get curated historical facts
        historical_facts = _get_curated_historical_facts(location_name, location_type)
        
        return {
            "historical_info": wikipedia_info,
            "cultural_events": cultural_info,
            "interesting_facts": historical_facts,
            "legends_and_stories": _get_madrid_legends(location_name),
            "source": "context_agent"
        }
        
    except Exception as e:
        logger.error(f"Error searching Madrid history: {e}")
        return {
            "historical_info": f"Información histórica de {location_name}",
            "cultural_events": [],
            "interesting_facts": [f"{location_name} es un lugar especial en Madrid"],
            "legends_and_stories": [],
            "source": "fallback"
        }

@tool
def get_current_events(location_name: str) -> List[Dict[str, Any]]:
    """
    Get current events and activities happening at or near the location.
    
    Args:
        location_name: Name of the location
        
    Returns:
        List of current events and activities
    """
    try:
        # Madrid Open Data - Cultural events
        events_url = "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json"
        
        response = requests.get(events_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current_events = []
        items = data.get("@graph", [])
        
        for item in items[:10]:  # Limit to 10 events
            event_info = _extract_event_info(item, location_name)
            if event_info:
                current_events.append(event_info)
        
        logger.info(f"Found {len(current_events)} current events for {location_name}")
        return current_events
        
    except Exception as e:
        logger.error(f"Error getting current events: {e}")
        return []

@tool
def search_family_activities(location_name: str, location_type: str) -> List[Dict[str, Any]]:
    """
    Search for family-friendly activities and recommendations.
    
    Args:
        location_name: Name of the location
        location_type: Type of location
        
    Returns:
        List of family activities and recommendations
    """
    try:
        activities = []
        
        # Get activities based on location type
        if location_type in ["museum", "cultural_center"]:
            activities.extend(_get_museum_family_activities(location_name))
        elif location_type in ["park", "garden"]:
            activities.extend(_get_park_family_activities(location_name))
        elif location_type in ["plaza", "monument"]:
            activities.extend(_get_historical_family_activities(location_name))
        
        # Add general Madrid family activities
        activities.extend(_get_general_madrid_activities())
        
        return activities[:8]  # Limit to 8 activities
        
    except Exception as e:
        logger.error(f"Error searching family activities: {e}")
        return []

# ===== HELPER FUNCTIONS =====

def _search_wikipedia(location_name: str) -> str:
    """Search Wikipedia for location information"""
    try:
        # Wikipedia API search
        search_url = "https://es.wikipedia.org/api/rest_v1/page/summary/"
        
        # Clean location name for Wikipedia search
        clean_name = location_name.replace(" de Madrid", "").replace("Madrid", "").strip()
        search_terms = [
            f"{clean_name} Madrid",
            clean_name,
            f"{location_name}"
        ]
        
        for term in search_terms:
            try:
                url = f"{search_url}{term.replace(' ', '_')}"
                response = requests.get(url, timeout=8)
                
                if response.status_code == 200:
                    data = response.json()
                    extract = data.get("extract", "")
                    if extract and len(extract) > 100:
                        logger.info(f"Found Wikipedia info for {term}")
                        return extract[:500] + "..." if len(extract) > 500 else extract
                        
            except Exception:
                continue
        
        return f"Información histórica disponible sobre {location_name}"
        
    except Exception as e:
        logger.error(f"Wikipedia search error: {e}")
        return f"Lugar histórico de Madrid: {location_name}"

def _search_madrid_cultural_data(location_name: str) -> List[Dict]:
    """Search Madrid Open Data for cultural information"""
    try:
        cultural_centers_url = "https://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.json"
        
        response = requests.get(cultural_centers_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        cultural_info = []
        items = data.get("@graph", [])
        
        for item in items:
            name = item.get("title", "")
            if isinstance(name, dict):
                name = name.get("es", name.get("@value", ""))
            
            if location_name.lower() in str(name).lower():
                cultural_info.append({
                    "name": str(name),
                    "description": item.get("description", ""),
                    "address": item.get("address", {})
                })
        
        return cultural_info[:3]  # Limit results
        
    except Exception as e:
        logger.error(f"Madrid cultural data search error: {e}")
        return []

def _get_curated_historical_facts(location_name: str, location_type: str) -> List[str]:
    """Get curated historical facts about Madrid locations"""
    
    facts_database = {
        "plaza mayor": [
            "La Plaza Mayor fue construida en el siglo XVII bajo el reinado de Felipe III",
            "En esta plaza se celebraban corridas de toros, ejecuciones públicas y mercados",
            "La Casa de la Panadería fue el primer edificio construido en la plaza",
            "Felipe II encargó su construcción al arquitecto Juan de Herrera"
        ],
        "palacio real": [
            "El Palacio Real tiene más de 3.400 habitaciones, más que Versalles",
            "Fue construido sobre las ruinas del antiguo Alcázar Real que se quemó en 1734",
            "Carlos III fue el primer rey que habitó en el palacio actual",
            "Su biblioteca contiene más de 300.000 volúmenes"
        ],
        "puerta del sol": [
            "Es el kilómetro cero de las carreteras radiales españolas",
            "El reloj de la Casa de Correos marca las campanadas de fin de año",
            "La Puerta del Sol original era una de las puertas de la muralla de Madrid",
            "El oso y el madroño es el símbolo de Madrid desde el siglo XIII"
        ],
        "parque del retiro": [
            "Fue creado en el siglo XVII como jardín real para Felipe IV",
            "El Palacio de Cristal se construyó para la Exposición de las Islas Filipinas de 1887",
            "Tiene más de 15.000 árboles de 167 especies diferentes",
            "La estatua del Ángel Caído es una de las pocas estatuas del diablo en el mundo"
        ],
        "museo del prado": [
            "Alberga la mayor colección de pintura española del mundo",
            "Fue diseñado por Juan de Villanueva como Gabinete de Ciencias Naturales",
            "Las Meninas de Velázquez es su obra más famosa",
            "Tiene más de 8.000 pinturas, aunque solo exhibe unas 1.300"
        ]
    }
    
    location_key = location_name.lower()
    for key in facts_database:
        if key in location_key:
            return facts_database[key]
    
    # Default facts for unknown locations
    return [
        f"{location_name} forma parte de la rica historia de Madrid",
        "Madrid ha sido la capital de España desde 1561",
        "Esta zona ha visto pasar siglos de historia española"
    ]

def _get_madrid_legends(location_name: str) -> List[str]:
    """Get legends and magical stories about Madrid locations"""
    
    legends_database = {
        "plaza mayor": [
            "Se dice que en las noches de luna llena, las estatuas de la plaza cobran vida",
            "Los antiguos madrileños creían que bajo la plaza había túneles secretos"
        ],
        "palacio real": [
            "Cuenta la leyenda que los fantasmas de los reyes antiguos pasean por sus salones",
            "Se dice que en la biblioteca hay libros que se escriben solos por las noches"
        ],
        "parque del retiro": [
            "Las hadas del Retiro protegen a todos los niños que juegan en el parque",
            "El estanque grande es hogar de sirenas que solo aparecen al amanecer"
        ],
        "puerta del sol": [
            "El oso del escudo de Madrid era en realidad un oso mágico que protegía la ciudad",
            "Se cuenta que quien toque el kilómetro cero puede pedir un deseo"
        ]
    }
    
    location_key = location_name.lower()
    for key in legends_database:
        if key in location_key:
            return legends_database[key]
    
    return [f"Las leyendas de {location_name} están esperando ser descubiertas"]

def _extract_event_info(item: Dict, location_name: str) -> Dict[str, Any]:
    """Extract relevant event information from Madrid Open Data"""
    try:
        title = item.get("title", "")
        if isinstance(title, dict):
            title = title.get("es", title.get("@value", ""))
        
        description = item.get("description", "")
        if isinstance(description, dict):
            description = description.get("es", description.get("@value", ""))
        
        # Check if event is relevant to location
        if (location_name.lower() in str(title).lower() or 
            location_name.lower() in str(description).lower()):
            
            return {
                "title": str(title),
                "description": str(description),
                "date": item.get("dtstart", ""),
                "location": item.get("location", {})
            }
        
        return None
        
    except Exception:
        return None

def _get_museum_family_activities(location_name: str) -> List[Dict[str, Any]]:
    """Get family activities for museums"""
    return [
        {
            "activity": "Búsqueda del tesoro artística",
            "description": f"Busca obras específicas en {location_name} siguiendo pistas",
            "age_range": "6-12 años",
            "duration": "45-60 minutos"
        },
        {
            "activity": "Dibuja como los maestros",
            "description": "Crea tu propia obra inspirada en las pinturas del museo",
            "age_range": "4-10 años", 
            "duration": "30 minutos"
        }
    ]

def _get_park_family_activities(location_name: str) -> List[Dict[str, Any]]:
    """Get family activities for parks"""
    return [
        {
            "activity": "Búsqueda de tesoros naturales",
            "description": f"Encuentra hojas, piedras y flores especiales en {location_name}",
            "age_range": "3-10 años",
            "duration": "30-45 minutos"
        },
        {
            "activity": "Picnic mágico",
            "description": "Crea historias mientras disfrutas de un picnic familiar",
            "age_range": "Todas las edades",
            "duration": "60+ minutos"
        }
    ]

def _get_historical_family_activities(location_name: str) -> List[Dict[str, Any]]:
    """Get family activities for historical places"""
    return [
        {
            "activity": "Viaje en el tiempo",
            "description": f"Imagina cómo era la vida en {location_name} hace siglos",
            "age_range": "6-12 años",
            "duration": "20-30 minutos"
        },
        {
            "activity": "Arquitectos por un día",
            "description": "Observa y dibuja los detalles arquitectónicos del lugar",
            "age_range": "8-14 años",
            "duration": "30 minutos"
        }
    ]

def _get_general_madrid_activities() -> List[Dict[str, Any]]:
    """Get general Madrid family activities"""
    return [
        {
            "activity": "Mapa del tesoro madrileño",
            "description": "Crea un mapa de todos los lugares mágicos que has visitado",
            "age_range": "5-12 años",
            "duration": "Variable"
        }
    ]

# ===== AGENTE DE CONTEXTO =====

class ContextRetrievalAgent:
    """
    Real LangGraph Agent for historical and cultural context retrieval
    """
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.tools = [search_madrid_history, get_current_events, search_family_activities]
        
    def _initialize_llm(self):
        """Initialize Groq LLM for the agent"""
        api_key = os.getenv("GROQ_API_KEY")
        # Return None if API key or ChatGroq isn't available; agent will fall back to non-LLM behavior
        if not api_key or ChatGroq is None:
            return None
        try:
            return ChatGroq(
                groq_api_key=api_key,
                model_name="llama-3.1-8b-instant",
                temperature=0.4,
                max_tokens=800
            )
        except Exception:
            return None
    
    def research_location_context(self, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to research historical and cultural context
        """
        try:
            location_name = location_data.get("place_name", "Madrid")
            location_type = location_data.get("place_type", "location")
            
            logger.info(f"🔍 Researching context for: {location_name}")
            
            # Step 1: Get historical information
            historical_info = search_madrid_history.invoke({
                "location_name": location_name,
                "location_type": location_type
            })
            
            # Step 2: Get current events
            current_events = get_current_events.invoke({
                "location_name": location_name
            })
            
            # Step 3: Get family activities
            family_activities = search_family_activities.invoke({
                "location_name": location_name,
                "location_type": location_type
            })
            
            # Synthesize context using LLM
            context_summary = self._synthesize_context(
                location_name, historical_info, current_events, family_activities
            )
            
            return {
                "location_name": location_name,
                "historical_context": historical_info,
                "current_events": current_events,
                "family_activities": family_activities,
                "context_summary": context_summary,
                "research_completed": True
            }
            
        except Exception as e:
            logger.error(f"Error in context research: {e}")
            return {
                "location_name": location_data.get("place_name", "Madrid"),
                "historical_context": {"historical_info": "Información disponible"},
                "current_events": [],
                "family_activities": [],
                "context_summary": f"Contexto básico para {location_data.get('place_name', 'Madrid')}",
                "research_completed": False,
                "error": str(e)
            }
    
    def _synthesize_context(self, location_name: str, historical_info: Dict, 
                          current_events: List, family_activities: List) -> str:
        """
        Use LLM to synthesize all context information
        """
        try:
            system_prompt = f"""
Eres un investigador experto en la historia y cultura de Madrid. Tu tarea es sintetizar información 
histórica y cultural sobre {location_name} de manera que sea útil para el Ratoncito Pérez al crear 
historias mágicas para familias.

Información disponible:
- Historia: {historical_info.get('historical_info', '')}
- Hechos interesantes: {historical_info.get('interesting_facts', [])}
- Leyendas: {historical_info.get('legends_and_stories', [])}
- Eventos actuales: {len(current_events)} eventos
- Actividades familiares: {len(family_activities)} actividades

Crea un resumen conciso (máximo 200 palabras) que destaque:
1. Los aspectos más interesantes para niños
2. Conexiones históricas relevantes
3. Elementos que pueden usarse en historias mágicas
4. Actividades recomendadas

El tono debe ser informativo pero mágico, apropiado para el Ratoncito Pérez.
"""
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Sintetiza el contexto para {location_name}")
            ])
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error synthesizing context: {e}")
            return f"Contexto histórico y cultural rico disponible para {location_name}"

# Create global instance
context_agent = ContextRetrievalAgent()
