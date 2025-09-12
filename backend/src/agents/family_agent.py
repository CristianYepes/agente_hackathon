"""
Family Dynamics & Content Adaptation Agent - Real LangGraph Agent
Rol: Psicólogo infantil virtual y adaptador de contenido
"""

from typing import Dict, Any, List
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import logging
import os

logger = logging.getLogger(__name__)

# ===== TOOLS PARA EL AGENTE =====

@tool
def analyze_family_dynamics(family_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze family composition and dynamics for content adaptation.
    
    Args:
        family_profile: Family information including children ages, interests, etc.
        
    Returns:
        Dictionary with family analysis and recommendations
    """
    try:
        children = family_profile.get("children", [])
        if not children:
            children = [{"age": 7, "name": "pequeño aventurero"}]  # Default
        
        # Convert Child objects to dictionaries if needed
        children_data = []
        for child in children:
            if hasattr(child, '__dict__'):  # If it's a Pydantic model
                child_dict = {
                    "age": getattr(child, 'age', 7),
                    "gender": getattr(child, 'gender', 'child'),
                    "name": getattr(child, 'name', None) or "aventurero"
                }
            else:  # If it's already a dict
                child_dict = child
            children_data.append(child_dict)
        
        ages = [child.get("age", 7) for child in children_data]
        min_age = min(ages)
        max_age = max(ages)
        age_span = max_age - min_age
        
        # Analyze family composition
        family_analysis = {
            "total_children": len(children_data),
            "age_range": {"min": min_age, "max": max_age, "span": age_span},
            "family_type": _determine_family_type(ages),
            "attention_span": _calculate_attention_span(ages),
            "language_complexity": _determine_language_level(ages),
            "activity_preferences": _analyze_activity_preferences(children_data, family_profile),
            "special_considerations": _get_special_considerations(ages, family_profile)
        }
        
        logger.info(f"Family analysis completed: {family_analysis['family_type']}, ages {min_age}-{max_age}")
        return family_analysis
        
    except Exception as e:
        logger.error(f"Error analyzing family dynamics: {e}")
        return {
            "total_children": 1,
            "age_range": {"min": 7, "max": 7, "span": 0},
            "family_type": "single_child",
            "attention_span": "medium",
            "language_complexity": "simple",
            "activity_preferences": ["explorar", "jugar"],
            "special_considerations": []
        }

@tool
def adapt_content_complexity(content: str, target_age: int, content_type: str = "story") -> str:
    """
    Adapt content complexity for specific age group.
    
    Args:
        content: Original content to adapt
        target_age: Target age for adaptation
        content_type: Type of content (story, activity, explanation)
        
    Returns:
        Adapted content string
    """
    try:
        if target_age <= 4:
            return _adapt_for_preschool(content, content_type)
        elif target_age <= 7:
            return _adapt_for_early_elementary(content, content_type)
        elif target_age <= 10:
            return _adapt_for_elementary(content, content_type)
        elif target_age <= 13:
            return _adapt_for_preteen(content, content_type)
        else:
            return _adapt_for_teen(content, content_type)
            
    except Exception as e:
        logger.error(f"Error adapting content: {e}")
        return content

@tool
def suggest_age_appropriate_activities(ages: List[int], location_type: str, interests: List[str] = None) -> List[Dict[str, Any]]:
    """
    Suggest activities appropriate for the age range and interests.
    
    Args:
        ages: List of children ages
        location_type: Type of location (museum, park, plaza, etc.)
        interests: List of family interests
        
    Returns:
        List of age-appropriate activities
    """
    try:
        min_age = min(ages)
        max_age = max(ages)
        interests = interests or []
        
        activities = []
        
        # Base activities by location type
        base_activities = _get_base_activities_by_location(location_type)
        
        # Filter and adapt activities by age
        for activity in base_activities:
            adapted_activity = _adapt_activity_for_ages(activity, min_age, max_age, interests)
            if adapted_activity:
                activities.append(adapted_activity)
        
        # Add age-specific activities
        age_specific = _get_age_specific_activities(min_age, max_age, location_type)
        activities.extend(age_specific)
        
        # Sort by appropriateness score
        activities.sort(key=lambda x: x.get("appropriateness_score", 0), reverse=True)
        
        return activities[:6]  # Return top 6 activities
        
    except Exception as e:
        logger.error(f"Error suggesting activities: {e}")
        return []

@tool
def calculate_engagement_strategies(family_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate strategies to maintain family engagement.
    
    Args:
        family_analysis: Analysis of family dynamics
        
    Returns:
        Dictionary with engagement strategies
    """
    try:
        family_type = family_analysis.get("family_type", "single_child")
        age_range = family_analysis.get("age_range", {"min": 7, "max": 7})
        attention_span = family_analysis.get("attention_span", "medium")
        
        strategies = {
            "interaction_frequency": _calculate_interaction_frequency(attention_span),
            "content_rotation": _determine_content_rotation(family_type, age_range),
            "participation_methods": _get_participation_methods(family_type),
            "motivation_techniques": _get_motivation_techniques(age_range),
            "break_recommendations": _get_break_recommendations(attention_span),
            "challenge_level": _determine_challenge_level(age_range)
        }
        
        return strategies
        
    except Exception as e:
        logger.error(f"Error calculating engagement strategies: {e}")
        return {
            "interaction_frequency": "every_5_minutes",
            "content_rotation": "story_activity_break",
            "participation_methods": ["questions", "games"],
            "motivation_techniques": ["praise", "discovery"],
            "break_recommendations": ["every_15_minutes"],
            "challenge_level": "moderate"
        }

# ===== HELPER FUNCTIONS =====

def _determine_family_type(ages: List[int]) -> str:
    """Determine family type based on children ages"""
    if len(ages) == 1:
        return "single_child"
    elif len(ages) == 2:
        age_diff = abs(ages[0] - ages[1])
        if age_diff <= 2:
            return "close_siblings"
        elif age_diff <= 5:
            return "mixed_age_siblings"
        else:
            return "wide_age_gap"
    else:
        return "large_family"

def _calculate_attention_span(ages: List[int]) -> str:
    """Calculate expected attention span based on ages"""
    avg_age = sum(ages) / len(ages)
    
    if avg_age <= 4:
        return "short"  # 5-10 minutes
    elif avg_age <= 7:
        return "medium"  # 10-20 minutes
    elif avg_age <= 10:
        return "long"  # 20-30 minutes
    else:
        return "extended"  # 30+ minutes

def _determine_language_level(ages: List[int]) -> str:
    """Determine appropriate language complexity"""
    min_age = min(ages)
    
    if min_age <= 4:
        return "very_simple"
    elif min_age <= 6:
        return "simple"
    elif min_age <= 9:
        return "moderate"
    elif min_age <= 12:
        return "complex"
    else:
        return "advanced"

def _analyze_activity_preferences(children: List[Dict], family_profile: Dict) -> List[str]:
    """Analyze activity preferences from family profile"""
    preferences = []
    
    # Get interests from family profile
    interests = family_profile.get("interests", [])
    preferences.extend(interests)
    
    # Add age-based preferences
    ages = [child.get("age", 7) for child in children]
    avg_age = sum(ages) / len(ages)
    
    if avg_age <= 5:
        preferences.extend(["juegos simples", "cuentos", "colores", "animales"])
    elif avg_age <= 8:
        preferences.extend(["aventuras", "misterios", "exploración", "juegos activos"])
    elif avg_age <= 12:
        preferences.extend(["desafíos", "historia", "ciencia", "competiciones"])
    else:
        preferences.extend(["cultura", "arte", "tecnología", "debates"])
    
    return list(set(preferences))  # Remove duplicates

def _get_special_considerations(ages: List[int], family_profile: Dict) -> List[str]:
    """Get special considerations for the family"""
    considerations = []
    
    min_age = min(ages)
    max_age = max(ages)
    age_span = max_age - min_age
    
    if min_age <= 3:
        considerations.append("Necesita actividades muy simples y cortas")
    
    if age_span > 5:
        considerations.append("Necesita actividades que funcionen para diferentes edades")
    
    if len(ages) > 3:
        considerations.append("Familia numerosa - actividades grupales")
    
    if max_age > 12:
        considerations.append("Incluir elementos para pre-adolescentes")
    
    return considerations

def _adapt_for_preschool(content: str, content_type: str) -> str:
    """Adapt content for preschool age (3-4 years)"""
    if content_type == "story":
        return f"¡Hola pequeñín! {content[:100]}... ¡Es mágico! 🌟"
    elif content_type == "activity":
        return f"Vamos a jugar: {content} ¡Será súper fácil! 🎈"
    else:
        return f"¿Sabes qué? {content[:80]}... ¡Increíble! ✨"

def _adapt_for_early_elementary(content: str, content_type: str) -> str:
    """Adapt content for early elementary (5-7 years)"""
    if content_type == "story":
        return f"¡Escucha esta aventura! {content[:200]}... ¿Quieres saber más? 🏰"
    elif content_type == "activity":
        return f"¡Misión especial! {content} ¿Estás listo para la aventura? 🎯"
    else:
        return f"¿Sabías que {content[:150]}? ¡Es fascinante! 🌈"

def _adapt_for_elementary(content: str, content_type: str) -> str:
    """Adapt content for elementary (8-10 years)"""
    if content_type == "story":
        return f"Aquí tienes una historia increíble: {content[:300]}... 🎭"
    elif content_type == "activity":
        return f"Desafío para exploradores: {content} 🗺️"
    else:
        return f"Dato curioso: {content[:200]} 🔍"

def _adapt_for_preteen(content: str, content_type: str) -> str:
    """Adapt content for preteens (11-13 years)"""
    if content_type == "story":
        return f"Historia fascinante: {content[:400]}... 📚"
    elif content_type == "activity":
        return f"Investigación especial: {content} 🕵️"
    else:
        return f"Información interesante: {content} 🧠"

def _adapt_for_teen(content: str, content_type: str) -> str:
    """Adapt content for teens (14+ years)"""
    return content  # Return original content for teens

def _get_base_activities_by_location(location_type: str) -> List[Dict[str, Any]]:
    """Get base activities by location type"""
    
    activities_db = {
        "museum": [
            {
                "name": "Búsqueda del tesoro artística",
                "description": "Encuentra obras específicas siguiendo pistas",
                "base_age": 6,
                "duration": 30
            },
            {
                "name": "Detective del arte",
                "description": "Observa detalles y resuelve misterios artísticos",
                "base_age": 8,
                "duration": 25
            }
        ],
        "park": [
            {
                "name": "Exploración natural",
                "description": "Descubre plantas, animales y elementos naturales",
                "base_age": 4,
                "duration": 20
            },
            {
                "name": "Gymkhana en el parque",
                "description": "Circuito de actividades físicas y mentales",
                "base_age": 6,
                "duration": 35
            }
        ],
        "plaza": [
            {
                "name": "Viaje en el tiempo",
                "description": "Imagina cómo era este lugar en el pasado",
                "base_age": 7,
                "duration": 20
            },
            {
                "name": "Arquitectos por un día",
                "description": "Observa y dibuja la arquitectura histórica",
                "base_age": 8,
                "duration": 25
            }
        ]
    }
    
    return activities_db.get(location_type, activities_db["plaza"])

def _adapt_activity_for_ages(activity: Dict, min_age: int, max_age: int, interests: List[str]) -> Dict[str, Any]:
    """Adapt activity for specific age range and interests"""
    base_age = activity.get("base_age", 7)
    
    # Check if activity is appropriate for age range
    if base_age > max_age + 2 or base_age < min_age - 2:
        return None
    
    # Calculate appropriateness score
    score = 10
    if min_age <= base_age <= max_age:
        score += 5
    
    # Check interest alignment
    for interest in interests:
        if interest.lower() in activity["description"].lower():
            score += 3
    
    # Adapt description for age group
    adapted_description = activity["description"]
    if min_age <= 5:
        adapted_description = f"¡Juego mágico! {adapted_description}"
    elif min_age <= 8:
        adapted_description = f"¡Aventura especial! {adapted_description}"
    
    return {
        **activity,
        "adapted_description": adapted_description,
        "appropriateness_score": score,
        "age_adapted": True
    }

def _get_age_specific_activities(min_age: int, max_age: int, location_type: str) -> List[Dict[str, Any]]:
    """Get activities specific to age range"""
    activities = []
    
    if min_age <= 5:
        activities.append({
            "name": "Juego de colores",
            "description": "Encuentra objetos de diferentes colores",
            "adapted_description": "¡Busca colores mágicos como el Ratoncito!",
            "appropriateness_score": 9,
            "duration": 15
        })
    
    if max_age >= 10:
        activities.append({
            "name": "Investigación histórica",
            "description": "Investiga datos históricos del lugar",
            "adapted_description": "Conviértete en detective de la historia",
            "appropriateness_score": 8,
            "duration": 30
        })
    
    return activities

def _calculate_interaction_frequency(attention_span: str) -> str:
    """Calculate how often to interact with family"""
    frequency_map = {
        "short": "every_3_minutes",
        "medium": "every_5_minutes", 
        "long": "every_8_minutes",
        "extended": "every_10_minutes"
    }
    return frequency_map.get(attention_span, "every_5_minutes")

def _determine_content_rotation(family_type: str, age_range: Dict) -> str:
    """Determine content rotation strategy"""
    if family_type == "wide_age_gap":
        return "alternating_age_focus"
    elif family_type == "large_family":
        return "group_then_individual"
    else:
        return "story_activity_break"

def _get_participation_methods(family_type: str) -> List[str]:
    """Get methods to encourage participation"""
    base_methods = ["preguntas", "juegos", "observación"]
    
    if family_type == "large_family":
        base_methods.extend(["turnos", "equipos"])
    elif family_type == "close_siblings":
        base_methods.extend(["competiciones amistosas", "colaboración"])
    
    return base_methods

def _get_motivation_techniques(age_range: Dict) -> List[str]:
    """Get motivation techniques for age range"""
    min_age = age_range.get("min", 7)
    
    if min_age <= 5:
        return ["elogios", "pegatinas", "celebraciones"]
    elif min_age <= 8:
        return ["aventuras", "misterios", "descubrimientos"]
    elif min_age <= 12:
        return ["desafíos", "competiciones", "logros"]
    else:
        return ["reconocimiento", "responsabilidades", "debate"]

def _get_break_recommendations(attention_span: str) -> List[str]:
    """Get break recommendations based on attention span"""
    break_map = {
        "short": ["cada_10_minutos", "cambio_actividad_frecuente"],
        "medium": ["cada_15_minutos", "variación_contenido"],
        "long": ["cada_20_minutos", "pausas_activas"],
        "extended": ["cada_30_minutos", "reflexión_grupal"]
    }
    return break_map.get(attention_span, ["cada_15_minutos"])

def _determine_challenge_level(age_range: Dict) -> str:
    """Determine appropriate challenge level"""
    min_age = age_range.get("min", 7)
    max_age = age_range.get("max", 7)
    
    if max_age <= 5:
        return "very_easy"
    elif max_age <= 8:
        return "easy"
    elif max_age <= 12:
        return "moderate"
    else:
        return "challenging"

# ===== AGENTE DE ADAPTACIÓN FAMILIAR =====

class FamilyDynamicsAgent:
    """
    Real LangGraph Agent for family dynamics analysis and content adaptation
    """
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.tools = [
            analyze_family_dynamics, 
            adapt_content_complexity, 
            suggest_age_appropriate_activities,
            calculate_engagement_strategies
        ]
        
    def _initialize_llm(self):
        """Initialize Groq LLM for the agent"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=600
        )
    
    def analyze_and_adapt(self, family_profile: Dict[str, Any], location_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to analyze family and provide adaptation recommendations
        """
        try:
            logger.info(f"👨‍👩‍👧‍👦 Family Agent analyzing profile with {len(family_profile.get('children', []))} children")
            
            # Step 1: Analyze family dynamics
            family_analysis = analyze_family_dynamics.invoke({
                "family_profile": family_profile
            })
            
            # Step 2: Calculate engagement strategies
            engagement_strategies = calculate_engagement_strategies.invoke({
                "family_analysis": family_analysis
            })
            
            # Step 3: Suggest age-appropriate activities
            children_ages = [child.get("age", 7) for child in family_profile.get("children", [])]
            location_type = location_data.get("place_type", "attraction")
            interests = family_profile.get("interests", [])
            
            activities = suggest_age_appropriate_activities.invoke({
                "ages": children_ages,
                "location_type": location_type,
                "interests": interests
            })
            
            return {
                "family_analysis": family_analysis,
                "engagement_strategies": engagement_strategies,
                "recommended_activities": activities,
                "adaptation_completed": True
            }
            
        except Exception as e:
            logger.error(f"Error in family analysis: {e}")
            return {
                "family_analysis": {"family_type": "default", "language_complexity": "simple"},
                "engagement_strategies": {"interaction_frequency": "every_5_minutes"},
                "recommended_activities": [],
                "adaptation_completed": False,
                "error": str(e)
            }

# Create global instance
family_agent = FamilyDynamicsAgent()
