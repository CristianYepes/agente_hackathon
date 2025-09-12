# backend/src/langgraph/narrative_flow.py
from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RatoncitoState(TypedDict):
    latitude: float
    longitude: float
    family_profile: Dict[str, Any]
    user_message: str
    is_first_interaction: bool
    conversation_count: int
    location_analysis: Dict[str, Any]
    historical_context: Dict[str, Any]
    family_adaptation: Dict[str, Any]
    weather_context: Dict[str, Any]
    time_context: Dict[str, Any]
    magical_response: str
    current_step: str
    error_message: str
    session_id: str

def location_intelligence_node(state: RatoncitoState) -> RatoncitoState:
    try:
        logger.info(f"🌍 Analyzing location: {state['latitude']}, {state['longitude']}")

        location_analysis = {
            "place_name": "Madrid Centro",
            "place_type": "historical_center",
            "significance": "Corazón histórico de Madrid",
            "nearby_attractions": ["Plaza Mayor", "Puerta del Sol", "Palacio Real"],
            "family_friendly": True
        }

        state["location_analysis"] = location_analysis
        state["current_step"] = "location_completed"

        logger.info(f"✅ Location analysis completed")

    except Exception as e:
        logger.error(f"❌ Error in location_intelligence_node: {e}")
        state["error_message"] = f"Location analysis failed: {str(e)}"
        state["current_step"] = "error"

    return state

def context_enrichment_node(state: RatoncitoState) -> RatoncitoState:
    try:
        logger.info("📚 Enriching with historical context")

        historical_context = {
            "historical_facts": [
                "Madrid fue fundada en el siglo IX por el emir Muhammad I",
                "La Plaza Mayor fue construida en el siglo XVII",
                "El Palacio Real tiene más de 3000 habitaciones"
            ],
            "legends": [
                "Se dice que en las noches de luna llena, se pueden escuchar los ecos de las antiguas celebraciones reales",
                "La leyenda cuenta que Felipe III ordenó construir la plaza tras soñar con un gran espacio donde todo Madrid pudiera reunirse",
                "Los vecinos cuentan que cada ventana de la plaza tiene una historia diferente que contar"
            ],
            "cultural_significance": "Símbolo del Madrid de los Austrias y corazón social de la ciudad"
        }

        state["historical_context"] = historical_context
        state["current_step"] = "context_completed"

        logger.info("✅ Historical context enriched")

    except Exception as e:
        logger.error(f"❌ Error in context_enrichment_node: {e}")
        state["error_message"] = f"Context enrichment failed: {str(e)}"
        state["current_step"] = "error"

    return state

def family_adaptation_node(state: RatoncitoState) -> RatoncitoState:
    try:
        logger.info("👨‍👩‍👧‍👦 Adapting content for family")

        family_profile = state["family_profile"]
        children = family_profile.get("children", [])

        adaptation = {
            "age_appropriate_content": True,
            "interactive_elements": [
                "Buscar detalles arquitectónicos",
                "Contar elementos decorativos",
                "Imaginar historias del pasado"
            ],
            "educational_value": "Historia de Madrid adaptada para niños",
            "engagement_level": "high" if len(children) > 0 else "medium"
        }

        state["family_adaptation"] = adaptation
        state["current_step"] = "family_completed"

        logger.info("✅ Family adaptation completed")

    except Exception as e:
        logger.error(f"❌ Error in family_adaptation_node: {e}")
        state["error_message"] = f"Family adaptation failed: {str(e)}"
        state["current_step"] = "error"

    return state

def weather_time_node(state: RatoncitoState) -> RatoncitoState:
    try:
        logger.info("🌤️ Getting weather and time context")

        import datetime

        weather_context = {
            "current_weather": "soleado",
            "temperature": "22°C",
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

        time_context = {
            "current_time": datetime.datetime.now().strftime("%H:%M"),
            "time_period": "día",
            "day_of_week": "lunes",
            "recommended_activities": ["Visitar monumentos", "Pasear por plazas"],
            "opening_status": "La mayoría de lugares están abiertos",
            "is_weekend": False,
            "season": "primavera"
        }

        state["weather_context"] = weather_context
        state["time_context"] = time_context
        state["current_step"] = "weather_completed"

        logger.info("✅ Weather and time context added")

    except Exception as e:
        logger.error(f"❌ Error in weather_time_node: {e}")
        state["error_message"] = f"Weather/time context failed: {str(e)}"
        state["current_step"] = "error"

    return state

def narrative_generation_node(state: RatoncitoState) -> RatoncitoState:
    try:
        logger.info("🐭 Generating magical response from Ratoncito Pérez")

        location = state["location_analysis"]
        historical = state["historical_context"]
        family = state["family_adaptation"]
        user_msg = state["user_message"]

        magical_response = f"""¡Hola pequeños aventureros! 🐭✨

Soy el Ratoncito Pérez y estoy encantado de encontraros en {location.get('place_name', 'Madrid')}.

{user_msg} - ¡Qué pregunta tan interesante!

¿Sabéis que {location.get('place_name', 'este lugar')} es muy especial? {historical.get('historical_facts', [''])[0] if historical.get('historical_facts') else 'Tiene una historia fascinante'}

Desde mi casita en la Calle Arenal, he visto muchas familias como la vuestra explorando Madrid. ¡Y siempre hay algo mágico que descubrir!

¿Queréis que os cuente un secreto? {historical.get('legends', ['Hay leyendas escondidas en cada rincón de Madrid'])[0] if historical.get('legends') else 'Este lugar guarda secretos increíbles'}

¡Sigamos explorando juntos! 🏰✨"""

        state["magical_response"] = magical_response
        state["current_step"] = "completed"

        logger.info("✅ Magical response generated")

    except Exception as e:
        logger.error(f"❌ Error in narrative_generation_node: {e}")
        state["error_message"] = f"Narrative generation failed: {str(e)}"
        state["current_step"] = "error"
        state["magical_response"] = "¡Ups! Tengo un pequeño problema técnico, pero estoy aquí para ayudaros. ¡Intentémoslo de nuevo! 🐭✨"

    return state

def should_continue(state: RatoncitoState) -> str:
    current_step = state.get("current_step", "start")

    if current_step == "error":
        return "narrative_generation"
    elif current_step == "location_completed":
        return "context_enrichment"
    elif current_step == "context_completed":
        return "family_adaptation"
    elif current_step == "family_completed":
        return "weather_time"
    elif current_step == "weather_completed":
        return "narrative_generation"
    elif current_step == "completed":
        return END
    else:
        return "location_intelligence"

workflow = StateGraph(RatoncitoState)

workflow.add_node("location_intelligence", location_intelligence_node)
workflow.add_node("context_enrichment", context_enrichment_node)
workflow.add_node("family_adaptation", family_adaptation_node)
workflow.add_node("weather_time", weather_time_node)
workflow.add_node("narrative_generation", narrative_generation_node)

workflow.set_entry_point("location_intelligence")

workflow.add_conditional_edges(
    "location_intelligence",
    should_continue,
    {
        "context_enrichment": "context_enrichment",
        "narrative_generation": "narrative_generation"
    }
)

workflow.add_conditional_edges(
    "context_enrichment",
    should_continue,
    {
        "family_adaptation": "family_adaptation",
        "narrative_generation": "narrative_generation"
    }
)

workflow.add_conditional_edges(
    "family_adaptation",
    should_continue,
    {
        "weather_time": "weather_time",
        "narrative_generation": "narrative_generation"
    }
)

workflow.add_conditional_edges(
    "weather_time",
    should_continue,
    {
        "narrative_generation": "narrative_generation",
        END: END
    }
)

workflow.add_conditional_edges(
    "narrative_generation",
    should_continue,
    {
        END: END
    }
)

memory = MemorySaver()
narrative_graph = workflow.compile(checkpointer=memory)

logger.info("🚀 Ratoncito Pérez LangGraph System initialized successfully")
