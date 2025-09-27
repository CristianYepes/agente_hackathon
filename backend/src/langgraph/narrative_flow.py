"""
Real LangGraph Multi-Agent System for Ratoncito Pérez - COMPLETE VERSION
AGENTES REALES con tool calling y flujo de estados completo
"""

from typing import Dict, Any, TypedDict
try:
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    LANGGRAPH_AVAILABLE = True
except Exception:
    # langgraph is optional for the full multi-agent workflow. Provide a fallback below.
    LANGGRAPH_AVAILABLE = False
import logging
import os

from src.agents.location_agent import location_agent
from src.agents.context_agent import context_agent
from src.agents.family_agent import family_agent
from src.agents.narrative_agent import ratoncito_agent
from src.tools.weather_tools import get_weather_context, get_time_context

logger = logging.getLogger(__name__)

# ===== ESTADO DEL GRAFO EXPANDIDO =====

class RatoncitoState(TypedDict):
    """Estado compartido entre todos los agentes"""
    # Input data
    latitude: float
    longitude: float
    family_profile: Dict[str, Any]
    user_message: str

    # Agent outputs
    location_analysis: Dict[str, Any]
    historical_context: Dict[str, Any]
    family_adaptation: Dict[str, Any]
    weather_context: Dict[str, Any]
    time_context: Dict[str, Any]
    magical_response: str

    # Control flow
    current_step: str
    error_message: str

# ===== NODOS DEL GRAFO (5 AGENTES REALES) =====

def location_intelligence_node(state: RatoncitoState) -> RatoncitoState:
    """
    Nodo 1: Location Intelligence Agent
    Analiza la ubicación GPS usando herramientas reales
    """
    try:
        logger.info(f"🌍 Location Agent analyzing: {state['latitude']}, {state['longitude']}")

        # Usar el agente real con tools
        location_analysis = location_agent.analyze_location(
            state["latitude"],
            state["longitude"]
        )

        state["location_analysis"] = location_analysis
        state["current_step"] = "location_completed"

        logger.info(f"✅ Location analysis completed for: {location_analysis.get('location_details', {}).get('place_name', 'Unknown')}")

    except Exception as e:
        logger.error(f"❌ Error in location_intelligence_node: {e}")
        state["error_message"] = f"Location analysis failed: {str(e)}"
        state["current_step"] = "error"

    return state

def context_retrieval_node(state: RatoncitoState) -> RatoncitoState:
    """
    Nodo 2: Context Retrieval Agent
    Investiga historia y contexto cultural del lugar
    """
    try:
        logger.info("🔍 Context Agent researching historical information...")

        location_data = state.get("location_analysis", {}).get("location_details", {})

        # Usar el agente de contexto real
        historical_context = context_agent.research_location_context(location_data)

        state["historical_context"] = historical_context
        state["current_step"] = "context_completed"

        logger.info(f"✅ Historical context gathered for: {historical_context.get('location_name', 'Unknown')}")

    except Exception as e:
        logger.error(f"❌ Error in context_retrieval_node: {e}")
        state["error_message"] = f"Context research failed: {str(e)}"
        state["current_step"] = "error"

    return state

def family_adaptation_node(state: RatoncitoState) -> RatoncitoState:
    """
    Nodo 3: Family Dynamics & Content Adaptation Agent
    Analiza dinámicas familiares y adapta contenido
    """
    try:
        logger.info("👨‍👩‍👧‍👦 Family Agent analyzing family dynamics...")

        family_profile = state.get("family_profile", {})
        location_data = state.get("location_analysis", {}).get("location_details", {})

        # Usar el agente de familia real
        family_adaptation = family_agent.analyze_and_adapt(family_profile, location_data)

        state["family_adaptation"] = family_adaptation
        state["current_step"] = "family_completed"

        family_type = family_adaptation.get("family_analysis", {}).get("family_type", "unknown")
        logger.info(f"✅ Family adaptation completed for: {family_type}")

    except Exception as e:
        logger.error(f"❌ Error in family_adaptation_node: {e}")
        state["error_message"] = f"Family adaptation failed: {str(e)}"
        state["current_step"] = "error"

    return state

def environmental_context_node(state: RatoncitoState) -> RatoncitoState:
    """
    Nodo 4: Environmental Context Agent
    Obtiene contexto climático y temporal
    """
    try:
        logger.info("🌤️ Environmental Agent gathering context...")

        # Get weather context
        weather_context = get_weather_context(state["latitude"], state["longitude"])
        time_context = get_time_context()

        state["weather_context"] = weather_context
        state["time_context"] = time_context
        state["current_step"] = "environmental_completed"

        logger.info(f"✅ Environmental context: {weather_context.get('condition', 'unknown')} weather")

    except Exception as e:
        logger.error(f"❌ Error in environmental_context_node: {e}")
        state["error_message"] = f"Environmental analysis failed: {str(e)}"
        state["current_step"] = "error"

    return state

def ratoncito_narrative_node(state: RatoncitoState) -> RatoncitoState:
    """
    Nodo 5: Ratoncito Pérez Narrative Agent
    Genera respuesta mágica final usando toda la información
    """
    try:
        logger.info("🐭 Ratoncito Agent creating magical response...")

        # Preparar todos los datos para el agente narrativo
        enhanced_location_data = {
            **state.get("location_analysis", {}),
            "historical_context": state.get("historical_context", {}),
        }

        # Usar el agente narrativo real con todos los contextos
        magical_response = ratoncito_agent.create_magical_response(
            location_data=enhanced_location_data,
            family_profile=state["family_profile"],
            weather_data=state.get("weather_context", {}),
            user_message=state["user_message"],
            family_adaptation=state.get("family_adaptation", {})
        )

        state["magical_response"] = magical_response
        state["current_step"] = "completed"

        logger.info("✅ Magical response generated successfully")

    except Exception as e:
        logger.error(f"❌ Error in ratoncito_narrative_node: {e}")
        state["error_message"] = f"Narrative generation failed: {str(e)}"
        state["current_step"] = "error"

    return state

def error_handler_node(state: RatoncitoState) -> RatoncitoState:
    """
    Nodo de manejo de errores
    """
    logger.warning(f"🚨 Error handler activated: {state.get('error_message', 'Unknown error')}")

    # Generate fallback response
    location_name = "Madrid"
    if state.get("location_analysis", {}).get("location_details"):
        location_name = state["location_analysis"]["location_details"].get("place_name", "Madrid")

    state["magical_response"] = f"""¡Hola, pequeños aventureros! 🐭✨

Soy el Ratoncito Pérez y aunque tengo un pequeño problema con mis herramientas mágicas, ¡la magia de {location_name} sigue aquí!

Este lugar está lleno de secretos y aventuras esperando a ser descubiertas. ¿Qué os gustaría explorar primero?

• Buscar pistas de tesoros escondidos
• Imaginar las historias que guardan estas piedras
• Descubrir rincones donde otros ratoncitos han estado

¡Contadme qué es lo que más os llama la atención! 💫
"""
    state["current_step"] = "completed"
    return state

# If langgraph isn't available, provide a minimal fallback graph implementation
if not LANGGRAPH_AVAILABLE:
    import logging
    logger.warning("langgraph no disponible; usando flujo de fallback simplificado para narrative_graph.")

    class FallbackNarrativeGraph:
        """Fallback graph when langgraph package is missing."""
        def process_request(self, latitude: float, longitude: float, family_profile: Dict[str, Any], user_message: str) -> str:
            # Simple deterministic response using inputs
            place = 'Madrid'
            try:
                # Try to read place name if provided in family_profile or user_message
                place = family_profile.get('place_name', place) if isinstance(family_profile, dict) else place
            except Exception:
                pass
            return (f"¡Hola! Soy el Ratoncito Pérez 🐭✨\n" 
                    f"Estáis en {place}. Gracias por escribir: '{user_message}'. \n" 
                    "Estoy usando un modo simplificado porque faltan herramientas internas, pero puedo seguir jugando y sugiriendo actividades. \n")

    # Export a simple instance compatible with the rest of the code
    narrative_graph = FallbackNarrativeGraph()

else:
    # ===== CONSTRUCCIÓN DEL GRAFO =====
    class RealRatoncitoGraph:
        """
        Sistema Multi-Agente REAL con LangGraph para Ratoncito Pérez - VERSION COMPLETA

        Flujo:
        GPS Input → Location Agent → Context Agent → Family Agent → Environmental Agent → Ratoncito Agent → Magic Response
        """

        def __init__(self):
            self.graph = self._build_graph()

        def _build_graph(self) -> StateGraph:
            """Construir el grafo de 5 agentes reales"""
            try:
                # Crear el grafo con estado
                workflow = StateGraph(RatoncitoState)

                # Añadir nodos
                workflow.add_node("location_intelligence", location_intelligence_node)
                workflow.add_node("context_retrieval", context_retrieval_node)
                workflow.add_node("family_adapt", family_adaptation_node)
                workflow.add_node("env_context", environmental_context_node)
                workflow.add_node("ratoncito_chat", ratoncito_narrative_node)
                workflow.add_node("error_handler", error_handler_node)

                # Definir el flujo secuencial
                workflow.set_entry_point("location_intelligence")

                # Flujo: Location → Context → Family → Environmental → Narrative
                workflow.add_conditional_edges(
                    "location_intelligence",
                    should_continue_to_context,
                    {"context_retrieval": "context_retrieval", "error_handler": "error_handler"}
                )

                workflow.add_conditional_edges(
                    "context_retrieval",
                    should_continue_to_family,
                    {"family_adapt": "family_adapt", "error_handler": "error_handler"}
                )

                workflow.add_conditional_edges(
                    "family_adapt",
                    should_continue_to_environmental,
                    {"env_context": "env_context", "error_handler": "error_handler"}
                )

                workflow.add_conditional_edges(
                    "env_context",
                    should_continue_to_narrative,
                    {"ratoncito_chat": "ratoncito_chat", "error_handler": "error_handler"}
                )

                workflow.add_conditional_edges(
                    "ratoncito_chat",
                    should_end,
                    {END: END}
                )

                workflow.add_conditional_edges(
                    "error_handler",
                    should_end,
                    {END: END}
                )

                # Compilar con memoria
                memory = MemorySaver()
                compiled_graph = workflow.compile(checkpointer=memory)
                logger.info("✅ Workflow compiled successfully")
                return compiled_graph

            except Exception as e:
                logger.error(f"❌ Workflow compilation failed: {e}")
                # Usar workflow mínimo de fallback
                return self._create_fallback_workflow()

        def _create_fallback_workflow(self):
            """Crear workflow simple de fallback"""
            workflow = StateGraph(RatoncitoState)
            workflow.add_node("simple_chat", self._simple_response_node)
            workflow.set_entry_point("simple_chat")
            workflow.add_edge("simple_chat", END)
            return workflow.compile()

        def _simple_response_node(self, state: RatoncitoState) -> RatoncitoState:
            """Nodo simple de respuesta cuando hay problemas con el workflow"""
            user_message = state.get("user_message", "")
            state["magical_response"] = f"¡Hola! Soy el Ratoncito Pérez 🐭✨ Has dicho: '{user_message}'. ¡Qué aventura queréis vivir en Madrid?"
            state["current_step"] = "completed"
            return state

        def process_request(self, latitude: float, longitude: float, family_profile: Dict[str, Any], user_message: str) -> str:
            try:
                # Estado inicial
                initial_state = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "family_profile": family_profile,
                    "user_message": user_message,
                    "location_analysis": {},
                    "historical_context": {},
                    "family_adaptation": {},
                    "weather_context": {},
                    "time_context": {},
                    "magical_response": "",
                    "current_step": "starting",
                    "error_message": ""
                }

                # Ejecutar el grafo de agentes
                config = {"configurable": {"thread_id": "ratoncito_session"}}

                logger.info("🚀 Starting Real Multi-Agent System...")
                logger.info(f"📍 Processing location: {latitude}, {longitude}")
                logger.info(f"👨‍👩‍👧‍👦 Family profile: {family_profile}")
                logger.info(f"💬 User message: {user_message}")

                final_state = self.graph.invoke(initial_state, config)

                # Extraer respuesta final
                response = final_state.get("magical_response", "¡Error mágico! Inténtalo de nuevo 🐭")

                logger.info("✅ Multi-Agent System completed successfully")
                return response

            except Exception as e:
                logger.error(f"❌ Error in multi-agent system: {e}")
                return f"""¡Hola, aventureros! 🐭✨

Soy el Ratoncito Pérez y aunque mis herramientas mágicas están teniendo un pequeño problema técnico, ¡la magia de Madrid sigue aquí!

Este lugar está lleno de secretos esperando ser descubiertos. ¿Qué aventura os gustaría vivir?

¡La magia nunca se detiene cuando hay corazones valientes como los vuestros! 💫

(Error técnico: {str(e)})
"""

    # ===== INSTANCIA GLOBAL =====

    # Crear instancia global del sistema multi-agente REAL
    real_narrative_graph = RealRatoncitoGraph()

    # Mantener compatibilidad con el código existente
    narrative_graph = real_narrative_graph

# ===== FUNCIONES DE FLUJO =====

def should_continue_to_context(state: RatoncitoState) -> str:
    """Decide si continuar al nodo de contexto o manejar error"""
    if state.get("current_step") == "error":
        return "error_handler"
    return "context_retrieval"

def should_continue_to_family(state: RatoncitoState) -> str:
    if state.get("current_step") == "error":
        return "error_handler"
    return "family_adapt"

def should_continue_to_environmental(state: RatoncitoState) -> str:
    if state.get("current_step") == "error":
        return "error_handler"
    return "env_context"

def should_continue_to_narrative(state: RatoncitoState) -> str:
    if state.get("current_step") == "error":
        return "error_handler"
    return "ratoncito_chat"

def should_end(state: RatoncitoState) -> str:
    """Decide si terminar el flujo"""
    return END


    def process_request(self, latitude: float, longitude: float, family_profile: Dict[str, Any], user_message: str) -> str:
        """
        Procesar solicitud completa usando el sistema multi-agente real

        Args:
            latitude: Latitud GPS
            longitude: Longitud GPS
            family_profile: Perfil familiar
            user_message: Mensaje del usuario

        Returns:
            Respuesta mágica del Ratoncito Pérez
        """
        try:
            # Estado inicial
            initial_state = {
                "latitude": latitude,
                "longitude": longitude,
                "family_profile": family_profile,
                "user_message": user_message,
                "location_analysis": {},
                "historical_context": {},
                "family_adaptation": {},
                "weather_context": {},
                "time_context": {},
                "magical_response": "",
                "current_step": "starting",
                "error_message": ""
            }

            # Ejecutar el grafo de agentes
            config = {"configurable": {"thread_id": "ratoncito_session"}}

            logger.info("🚀 Starting Real Multi-Agent System...")
            logger.info(f"📍 Processing location: {latitude}, {longitude}")
            logger.info(f"👨‍👩‍👧‍👦 Family profile: {family_profile}")
            logger.info(f"💬 User message: {user_message}")

            final_state = self.graph.invoke(initial_state, config)

            # Extraer respuesta final
            response = final_state.get("magical_response", "¡Error mágico! Inténtalo de nuevo 🐭")

            logger.info("✅ Multi-Agent System completed successfully")
            return response

        except Exception as e:
            logger.error(f"❌ Error in multi-agent system: {e}")
            return f"""¡Hola, aventureros! 🐭✨

Soy el Ratoncito Pérez y aunque mis herramientas mágicas están teniendo un pequeño problema técnico, ¡la magia de Madrid sigue aquí!

Este lugar está lleno de secretos esperando ser descubiertos. ¿Qué aventura os gustaría vivir?

¡La magia nunca se detiene cuando hay corazones valientes como los vuestros! 💫

(Error técnico: {str(e)})
"""

# ===== INSTANCIA GLOBAL =====

# Crear instancia global del sistema multi-agente REAL solo si langgraph está disponible
if LANGGRAPH_AVAILABLE:
    real_narrative_graph = RealRatoncitoGraph()
    # Mantener compatibilidad con el código existente
    narrative_graph = real_narrative_graph
else:
    # Cuando langgraph no está disponible ya exportamos `narrative_graph` como
    # una instancia de `FallbackNarrativeGraph` más arriba, así que no es necesario
    # crear la versión real.
    pass
