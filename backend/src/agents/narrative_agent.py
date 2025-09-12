"""
Narrative & Activity Generation Agent - Ratoncito Pérez
Rol: Narrador mágico y coordinador de actividades
"""

from typing import Dict, Any, List
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import logging
import os
import random

logger = logging.getLogger(__name__)

# ===== TOOLS PARA EL AGENTE RATONCITO =====

@tool
def generate_magic_story(location_info: Dict, family_profile: Dict) -> str:
    """
    Generate a magical story about the Ratoncito Pérez for the specific location.
    
    Args:
        location_info: Complete location information including address, area description, etc.
        family_profile: Information about the family (ages, interests, etc.)
        
    Returns:
        Magical story string personalized for the location and family
    """
    try:
        # Extract location details
        location_name = location_info.get("formatted_address", "Madrid")
        street = location_info.get("street", "")
        district = location_info.get("district", "Centro")
        area_desc = location_info.get("area_description", "en Madrid")
        
        # Determine story context
        story_context = "street"
        if any(word in location_name.lower() for word in ["plaza", "square"]):
            story_context = "plaza"
        elif any(word in location_name.lower() for word in ["museo", "museum", "palacio", "palace"]):
            story_context = "museum"
        elif any(word in location_name.lower() for word in ["parque", "park", "jardín", "garden"]):
            story_context = "park"
        elif any(word in location_name.lower() for word in ["calle", "avenida", "gran vía"]):
            story_context = "street"
        
        # Generate personalized story
        child_ages = family_profile.get("children_ages", [7])
        oldest_child = max(child_ages) if child_ages else 7
        
        # Base stories enhanced with real location details
        stories_by_type = {
            "plaza": [
                f"¡Qué emocionante! Estamos {area_desc}, en una de mis plazas favoritas de Madrid. Aquí, bajo estas piedras históricas, tengo una de mis guaridas más antiguas. Cuando los niños madrileños vienen a jugar y pierden sus dientes, ¡yo aparezco por la noche corriendo por estos adoquines mágicos!",
                f"Esta plaza ha visto pasar siglos de historia, y yo he estado aquí todo este tiempo. Los dientes que caen aquí se convierten en monedas especiales que brillan con la luz de las farolas antiguas. ¡{district} siempre ha sido territorio del Ratoncito Pérez!",
            ],
            "museum": [
                f"¡Estamos {area_desc}! Este lugar guarda secretos que solo yo, el Ratoncito Pérez, conozco. Por las noches, cuando todo está silencioso, las obras de arte me ayudan a encontrar los dientes perdidos de los pequeños visitantes más curiosos.",
                f"Una vez, un niño de {oldest_child} años perdió su diente aquí mismo. Las estatuas me susurraron dónde había caído, ¡y le dejé una moneda mágica que cambió de color cada noche durante una semana! En {district} pasan las cosas más maravillosas.",
            ],
            "park": [
                f"¡Qué lugar tan especial para estar {area_desc}! Los árboles de aquí son mis amigos más antiguos. Me cuentan historias de niños valientes que han perdido sus dientes jugando en estos senderos. Cada hoja que susurra lleva el nombre de un pequeño madrileño.",
                f"Este parque es mágico para el Ratoncito Pérez. Los pájaros son mis mensajeros especiales - cuando un niño pierde un diente corriendo por aquí, ellos me cantan la ubicación exacta. ¡En {district} la naturaleza y la magia van de la mano!",
            ],
            "street": [
                f"¡Estamos {area_desc}! {street if street else 'Esta calle'} es uno de mis caminos nocturnos favoritos. Mis patitas diminutas han corrido por estas piedras miles de veces, buscando dientes de niños aventureros que exploran Madrid.",
                f"Las farolas de esta zona son especiales - me iluminan cuando vengo de noche a recoger dientes. Una vez encontré aquí el diente de una niña muy valiente, ¡y le dejé una moneda que brillaba igual que las luces de {district}!",
            ]
        }
        
        # Select and personalize story
        base_stories = stories_by_type.get(story_context, stories_by_type["street"])
        selected_story = random.choice(base_stories)
        
        # Add family personalization
        if oldest_child <= 5:
            ending = " ¡Y ahora tengo que irme volando, pero recuerda siempre cepillarte los dientes para que estén limpitos cuando me los traigas!"
        elif oldest_child <= 8:
            ending = f" ¡Seguro que un niño valiente de {oldest_child} años como tú me traerá pronto algún diente especial!"
        else:
            ending = " ¡Quizás ya seas mayor para el Ratoncito Pérez, pero puedes ayudar a los más pequeños a cuidar sus dientes!"
        
        full_story = selected_story + ending
        
        logger.info(f"Generated magical story for {location_name} with {story_context} context")
        return full_story
        
    except Exception as e:
        logger.error(f"Error generating magic story: {e}")
        return "¡Hola! Soy el Ratoncito Pérez y me alegra mucho conocerte aquí en Madrid. Esta ciudad está llena de magia y aventuras esperándote. ¡Cuida bien tus dientes y quizás pronto me visites!"
        
        # Select appropriate story based on location type
        story_key = "street"  # default
        for key in stories_by_type.keys():
            if key in location_type.lower():
                story_key = key
                break
        
        stories = stories_by_type.get(story_key, stories_by_type["street"])
        base_story = random.choice(stories)
        
        # Add family-specific elements
        ages = family_profile.get("children_ages", [])
        if ages:
            min_age = min(ages)
            if min_age <= 6:
                base_story += " ¡Los ratoncitos más pequeños como vosotros sois mis favoritos porque creéis en la magia de verdad!"
            elif min_age <= 10:
                base_story += " A los aventureros de vuestra edad les encanta descubrir los secretos que escondo por Madrid."
            else:
                base_story += " Los exploradores mayores como vosotros podéis ayudarme a encontrar pistas históricas muy especiales."
        
        return base_story
        
    except Exception as e:
        logger.error(f"Error generating magic story: {e}")
        return f"¡Bienvenidos a {location_name}! Este lugar está lleno de magia y secretos que solo el Ratoncito Pérez conoce."

@tool  
def suggest_family_activities(location_data: Dict, family_profile: Dict, weather_condition: str = "pleasant") -> List[Dict[str, str]]:
    """
    Suggest age-appropriate activities for the family at the current location, prioritizing cultural sites.
    
    Args:
        location_data: Information about the current location
        family_profile: Family composition and preferences
        weather_condition: Current weather condition
        
    Returns:
        List of activity suggestions with descriptions
    """
    try:
        location_name = location_data.get("place_name", "Madrid")
        nearby_pois = location_data.get("nearby_pois", [])
        
        ages = family_profile.get("children_ages", [6])
        min_age = min(ages) if ages else 6
        max_age = max(ages) if ages else 12
        
        activities = []
        
        # Prioritize cultural and historical POIs
        museums = [poi for poi in nearby_pois if poi["type"] == "museum"]
        monuments = [poi for poi in nearby_pois if poi["type"] == "monument"] 
        parks = [poi for poi in nearby_pois if poi["type"] == "park"]
        cultural_centers = [poi for poi in nearby_pois if poi["type"] == "cultural_center"]
        
        # Activities based on nearby REAL cultural sites
        for museum in museums[:2]:
            activities.append({
                "activity": f"Exploración del {museum['name']}",
                "description": f"Visita guiada familiar al {museum['name']}. Buscad pistas históricas y tesoros culturales que solo los niños curiosos pueden encontrar.",
                "age_range": f"{min_age}-{max_age} años",
                "magic_element": f"El Ratoncito Pérez conoce secretos especiales guardados en {museum['name']}.",
                "real_location": True,
                "distance": museum.get('distance_km', 0)
            })
        
        for monument in monuments[:2]:
            activities.append({
                "activity": f"Aventura en {monument['name']}",
                "description": f"Descubre los misterios de {monument['name']}. Contad las ventanas, buscad escudos antiguos y escuchad las historias que susurran las piedras.",
                "age_range": f"{min_age}-{max_age} años",
                "magic_element": f"En {monument['name']}, el Ratoncito ha guardado muchos dientes de pequeños príncipes y princesas.",
                "real_location": True,
                "distance": monument.get('distance_km', 0)
            })
        
        for park in parks[:1]:
            activities.append({
                "activity": f"Búsqueda del tesoro en {park['name']}",
                "description": f"Explorad {park['name']} siguiendo las pistas del Ratoncito. Recoged hojas especiales y buscad árboles con formas mágicas.",
                "age_range": f"{min_age}-{max_age} años",
                "magic_element": f"Los árboles de {park['name']} guardan mensajes secretos para los niños aventureros.",
                "real_location": True,
                "distance": park.get('distance_km', 0)
            })
        
        # Add generic location-based activities if we have few real POIs
        if len(activities) < 3:
            # Determine general area type for appropriate activities
            location_type = location_data.get("place_type", "").lower()
            
            if any(word in location_name.lower() for word in ["plaza", "square"]):
                activities.append({
                    "activity": "Contador de Secretos de Plaza",
                    "description": f"En esta plaza histórica, contad elementos arquitectónicos: balcones, farolas, ventanas... Cada número tiene un significado mágico.",
                    "age_range": f"{min_age}-{max_age} años",
                    "magic_element": "Las plazas de Madrid son lugares donde se cruzan los caminos de todos los ratoncitos de la ciudad.",
                    "real_location": False
                })
            
            if any(word in location_name.lower() for word in ["calle", "street", "avenida"]):
                activities.append({
                    "activity": "Detective de Historias Urbanas",
                    "description": f"Observad las fachadas de los edificios. Buscad fechas, escudos o detalles curiosos que nos cuenten la historia del barrio.",
                    "age_range": f"{min_age}-{max_age} años",
                    "magic_element": "Cada calle de Madrid tiene una historia que el Ratoncito conoce desde hace siglos.",
                    "real_location": False
                })
        
        # Weather-specific activities
        if weather_condition in ["rain", "cloudy"]:
            activities.append({
                "activity": "Refugio de Exploradores",
                "description": "Buscad portales, soportales o entradas con historia donde refugiarse y observar la arquitectura tradicional madrileña.",
                "age_range": f"{min_age}-{max_age} años",
                "magic_element": "Los días nublados revelan detalles arquitectónicos que el sol esconde.",
                "real_location": False
            })
        elif weather_condition in ["sunny", "clear"]:
            activities.append({
                "activity": "Cazadores de Sombras Históricas",
                "description": "Observad cómo las sombras revelan formas en monumentos y edificios. El sol es el mejor guía turístico.",
                "age_range": f"{min_age}-{max_age} años",
                "magic_element": "El sol de Madrid ilumina secretos que solo aparecen a ciertas horas del día.",
                "real_location": False
            })
        
        # Sort by real locations first, then by distance
        activities.sort(key=lambda x: (not x.get("real_location", False), x.get("distance", 999)))
        
        return activities[:4]  # Return top 4 activities
        
    except Exception as e:
        logger.error(f"Error suggesting activities: {e}")
        return [
            {
                "activity": "Exploración Cultural",
                "description": f"Explorad {location_data.get('place_name', 'este lugar histórico')} con curiosidad. Buscad detalles arquitectónicos y elementos que cuenten la historia del lugar.",
                "age_range": f"{min(family_profile.get('children_ages', [6]))}-{max(family_profile.get('children_ages', [12]))} años",
                "magic_element": "Todo rincón de Madrid guarda secretos para los exploradores más curiosos.",
                "real_location": False
            }
        ]

def _is_age_appropriate(age_range_str: str, min_age: int, max_age: int) -> bool:
    """Check if activity is appropriate for the family's age range"""
    try:
        if "años" in age_range_str:
            range_part = age_range_str.split(" años")[0]
            if "-" in range_part:
                activity_min, activity_max = map(int, range_part.split("-"))
                return not (max_age < activity_min or min_age > activity_max)
        return True
    except:
        return True

@tool
def create_personalized_greeting(family_profile: Dict, location_name: str) -> str:
    """
    Create a personalized greeting from Ratoncito Pérez.
    
    Args:
        family_profile: Information about the family
        location_name: Current location name
        
    Returns:
        Personalized greeting string
    """
    try:
        ages = family_profile.get("children_ages", [])
        names = family_profile.get("children_names", [])
        interests = family_profile.get("interests", [])
        
        greeting_base = "¡Hola, pequeños aventureros mágicos! 🐭✨"
        
        # Personalize by names if available
        if names:
            if len(names) == 1:
                greeting_base = f"¡Hola, {names[0]}! Soy vuestro amigo el Ratoncito Pérez 🐭✨"
            else:
                greeting_base = f"¡Hola, {', '.join(names[:-1])} y {names[-1]}! Soy vuestro amigo el Ratoncito Pérez 🐭✨"
        
        # Add age-specific elements
        if ages:
            min_age = min(ages)
            if min_age <= 5:
                greeting_base += " ¡Qué emocionante tener ratoncitos tan pequeñitos y valientes aquí!"
            elif min_age <= 8:
                greeting_base += " ¡Perfecta edad para las aventuras más mágicas de Madrid!"
            else:
                greeting_base += " ¡Grandes exploradores listos para descubrir secretos increíbles!"
        
        # Add location element
        greeting_base += f" Me alegra muchísimo encontraros en {location_name}."
        
        # Add interest-based element
        if "history" in interests:
            greeting_base += " Veo que os gusta la historia, ¡este lugar está lleno de secretos antiguos!"
        elif "adventure" in interests:
            greeting_base += " ¡Aventureros como vosotros son mis favoritos para las misiones especiales!"
        elif "nature" in interests:
            greeting_base += " Los amantes de la naturaleza siempre encuentran la magia más pura."
        
        return greeting_base
        
    except Exception as e:
        logger.error(f"Error creating greeting: {e}")
        return f"¡Hola, aventureros! Soy el Ratoncito Pérez y me alegra encontraros en {location_name} 🐭✨"

# ===== AGENTE NARRATIVE (RATONCITO PÉREZ) =====

class RatoncitoNarrativeAgent:
    """
    Real LangGraph Agent - Ratoncito Pérez Narrative Generator
    Combines location data, family profile, and magical storytelling
    """
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.tools = [generate_magic_story, suggest_family_activities, create_personalized_greeting]
        
    def _initialize_llm(self):
        """Initialize Groq LLM for the Ratoncito agent"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.8,  # Higher creativity for storytelling
            max_tokens=1200
        )
    
    def create_magical_response(self, location_data: Dict, family_profile: Dict, 
                              weather_data: Dict, user_message: str, family_adaptation: Dict = None,
                              is_first_interaction: bool = True) -> str:
        """
        Main method to create enhanced magical response as Ratoncito Pérez
        
        Args:
            location_data: Location analysis with historical context
            family_profile: Family information
            weather_data: Weather context
            user_message: User's input message
            family_adaptation: Family dynamics analysis (optional)
            is_first_interaction: Whether this is the first interaction (controls greeting)
            
        Returns:
            Enhanced magical response string from Ratoncito Pérez
        """
        try:
            # Extract enhanced information
            location_details = location_data.get("location_details", {})
            historical_context = location_data.get("historical_context", {})
            
            location_name = location_details.get("place_name", "Madrid")
            location_type = location_details.get("place_type", "lugar")
            
            logger.info(f"🐭 Creating enhanced magical response for {location_name}")
            
            # Step 1: Generate personalized greeting (only for first interaction)
            greeting = ""
            if is_first_interaction:
                greeting = create_personalized_greeting.invoke({
                    "family_profile": family_profile,
                    "location_name": location_name
                })
            
            # Step 2: Generate magic story with historical context
            enhanced_location_info = {
                **location_details,
                "historical_info": historical_context.get("historical_context", {}).get("historical_info", ""),
                "interesting_facts": historical_context.get("historical_context", {}).get("interesting_facts", []),
                "legends": historical_context.get("historical_context", {}).get("legends_and_stories", [])
            }
            
            magic_story = generate_magic_story.invoke({
                "location_info": enhanced_location_info,
                "family_profile": family_profile
            })
            
            # Step 3: Get activities (enhanced or basic)
            if family_adaptation and family_adaptation.get("recommended_activities"):
                activities = family_adaptation["recommended_activities"]
            else:
                activities = suggest_family_activities.invoke({
                    "location_data": location_data,
                    "family_profile": family_profile,
                    "weather_condition": weather_data.get("condition", "pleasant")
                })
            
            # Step 4: Create enhanced magical response
            complete_response = self._synthesize_enhanced_magical_response(
                greeting, magic_story, activities, location_data, 
                historical_context, weather_data, family_adaptation, user_message,
                is_first_interaction
            )
            
            return complete_response
            
        except Exception as e:
            logger.error(f"Error creating enhanced magical response: {e}")
            return f"¡Hola, pequeños aventureros! Soy el Ratoncito Pérez y aunque tengo un pequeño problema técnico, ¡la magia de {location_data.get('place_name', 'Madrid')} sigue aquí! ✨"
    
    def _synthesize_enhanced_magical_response(self, greeting: str, story: str, activities: List[Dict],
                                            location_data: Dict, historical_context: Dict, 
                                            weather_data: Dict, family_adaptation: Dict, user_message: str,
                                            is_first_interaction: bool = True) -> str:
        """
        Use LLM to create enhanced cohesive magical response with all contexts
        """
        try:
            # Prepare context information
            location_name = location_data.get("location_details", {}).get("place_name", "Madrid")
            historical_info = historical_context.get("historical_context", {})
            interesting_facts = historical_info.get("interesting_facts", [])
            legends = historical_info.get("legends_and_stories", [])
            
            family_info = ""
            if family_adaptation:
                family_analysis = family_adaptation.get("family_analysis", {})
                family_type = family_analysis.get("family_type", "familia")
                age_range = family_analysis.get("age_range", {})
                family_info = f"Familia {family_type}, edades {age_range.get('min', 7)}-{age_range.get('max', 7)}"
            
            activity_list = "\n".join([f"• {act.get('name', act.get('activity', 'Actividad'))}: {act.get('description', act.get('adapted_description', ''))}" 
                                     for act in activities[:4]])
            
            system_prompt = f"""
Eres el Ratoncito Pérez, el personaje mágico más querido de Madrid. Tu personalidad es:
- Cariñoso y cercano con los niños y familias
- Lleno de imaginación y magia
- Conocedor de todos los secretos e historia de Madrid
- Entusiasta y aventurero
- Siempre positivo y alentador

CONTEXTO DE LA UBICACIÓN:
- Lugar: {location_name}
- Datos históricos interesantes: {interesting_facts[:2] if interesting_facts else ['Lugar lleno de historia']}
- Leyendas locales: {legends[:1] if legends else ['Leyendas por descubrir']}
- Familia: {family_info}
- Clima: {weather_data.get('condition', 'agradable')}

ELEMENTOS DISPONIBLES:
{"1. Saludo: " + greeting[:100] + "..." if is_first_interaction and greeting else ""}
2. Historia mágica: {story[:150]}...
3. Actividades sugeridas:
{activity_list}

INSTRUCCIONES:
Tu respuesta debe:
{"1. Incorporar el saludo personalizado de forma natural (SOLO SI ES PRIMERA INTERACCIÓN)" if is_first_interaction else "1. NO incluir saludo largo, responder directamente"}
2. Tejer la historia mágica con datos históricos reales
3. Responder específicamente al mensaje del usuario: "{user_message}"
4. Sugerir 2-3 actividades de forma emocionante
5. Usar hechos históricos para enriquecer la narrativa
6. Mantener el tono mágico pero incluir información real
7. Usar emojis apropiados (🐭✨🏰🌟💫)
8. Terminar con una invitación a la aventura

{"IMPORTANTE: Esta es la PRIMERA interacción, usa el saludo completo." if is_first_interaction else "IMPORTANTE: Esta NO es la primera interacción, NO uses saludo largo, responde directamente como si ya nos conocemos."}

Máximo 400 palabras. NO menciones errores técnicos. TODO es magia pura.
"""
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Usuario dice: '{user_message}' en {location_name}")
            ])
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error synthesizing enhanced response: {e}")
            return f"{greeting}\n\n{story}\n\n¡Vamos a explorar {location_data.get('place_name', 'Madrid')} juntos! ✨"

    def _synthesize_magical_response(self, greeting: str, story: str, activities: List[Dict],
                                   location_data: Dict, weather_data: Dict, user_message: str) -> str:
        """
        Use LLM to create a cohesive magical response
        """
        try:
            system_prompt = """
Eres el Ratoncito Pérez, el personaje mágico más querido de Madrid. Tu personalidad es:
- Cariñoso y cercano con los niños
- Lleno de imaginación y magia
- Conocedor de todos los secretos de Madrid
- Entusiasta y aventurero
- Siempre positivo y alentador

Tu respuesta debe:
1. Usar el saludo personalizado
2. Incorporar la historia mágica del lugar
3. Responder específicamente al mensaje del usuario
4. Sugerir actividades de forma natural y emocionante
5. Mantener el tono mágico y familiar
6. Usar emojis apropiados (🐭✨🏰🌟💫)
7. Terminar con una pregunta o invitación a la aventura

NO menciones errores técnicos o limitaciones. TODO es magia pura.
"""
            
            activities_text = "\n".join([
                f"• {act['activity']}: {act['description']}"
                for act in activities[:3]
            ])
            
            user_prompt = f"""
SALUDO PERSONALIZADO: {greeting}

HISTORIA MÁGICA DEL LUGAR: {story}

ACTIVIDADES SUGERIDAS:
{activities_text}

CONTEXTO DEL LUGAR:
- Ubicación: {location_data.get('place_name', 'Madrid')}
- Análisis: {location_data.get('analysis', 'Un lugar lleno de magia')}

CLIMA ACTUAL: {weather_data.get('condition', 'agradable')}, {weather_data.get('temperature', 20)}°C

MENSAJE DEL USUARIO: "{user_message}"

Crea una respuesta mágica y cohesiva del Ratoncito Pérez que responda al usuario e integre todos estos elementos de forma natural.
"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error in LLM synthesis: {e}")
            return f"{greeting}\n\n{story}\n\n¡Hay tantas aventuras esperándoos aquí! ¿Qué os gustaría explorar primero? 🐭✨"

# Global instance
ratoncito_agent = RatoncitoNarrativeAgent()
