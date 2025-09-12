from typing import Dict, List
from ..api.models import Child, FamilyProfile

def adapt_content_for_age(content: str, child_age: int, child_gender: str) -> str:
    """
    Adapt content complexity and themes based on child's age and gender
    """
    # Age-based adaptation
    if child_age <= 5:
        # Very simple language, short sentences, basic concepts
        complexity = "simple"
        max_length = 100
    elif child_age <= 8:
        # Moderate complexity, adventure themes
        complexity = "moderate"
        max_length = 200
    else:
        # More detailed, historical facts mixed with fantasy
        complexity = "advanced"
        max_length = 300
    
    # Gender-based theme adaptation (while being inclusive)
    gender_themes = get_gender_themes(child_gender, child_age)
    
    # Apply adaptations
    adapted_content = apply_complexity_adaptation(content, complexity, max_length)
    adapted_content = apply_theme_adaptation(adapted_content, gender_themes, child_age)
    
    return adapted_content

def get_gender_themes(gender: str, age: int) -> Dict[str, List[str]]:
    """
    Get appropriate themes based on gender preferences (while being inclusive)
    """
    base_themes = {
        "universal": ["aventura", "misterio", "tesoros", "animales", "magia", "amistad"],
        "historical": ["caballeros", "exploradores", "artistas", "inventores"],
        "activities": ["buscar pistas", "resolver acertijos", "contar historias"]
    }
    
    if gender.lower() == "girl":
        base_themes.update({
            "characters": ["princesas", "reinas", "hadas", "brujas buenas", "artistas"],
            "themes": ["vestidos históricos", "jardines mágicos", "bailes reales", "arte y belleza"],
            "activities": ["crear historias", "imaginar vestidos", "buscar flores", "dibujar"]
        })
    elif gender.lower() == "boy":
        base_themes.update({
            "characters": ["caballeros", "exploradores", "magos", "soldados valientes", "artesanos"],
            "themes": ["batallas históricas", "construcciones", "herramientas antiguas", "aventuras"],
            "activities": ["explorar", "construir", "buscar armas antiguas", "competiciones"]
        })
    else:
        # Gender-neutral or other
        base_themes.update({
            "characters": ["exploradores", "magos", "artistas", "inventores", "guardianes"],
            "themes": ["descubrimientos", "creaciones", "naturaleza", "ciencia antigua"],
            "activities": ["experimentar", "descubrir", "crear", "explorar libremente"]
        })
    
    return base_themes

def apply_complexity_adaptation(content: str, complexity: str, max_length: int) -> str:
    """
    Adapt language complexity based on age
    """
    if complexity == "simple":
        # Simple words, present tense, direct sentences
        simplified = content.replace("extraordinario", "increíble")
        simplified = simplified.replace("magnífico", "genial")
        simplified = simplified.replace("construyeron", "hicieron")
        return simplified[:max_length] + "..." if len(simplified) > max_length else simplified
        
    elif complexity == "moderate":
        # Add some adventure vocabulary but keep it accessible
        return content[:max_length] + "..." if len(content) > max_length else content
        
    else:
        # Advanced - can include historical terms and complex concepts
        return content

def apply_theme_adaptation(content: str, themes: Dict[str, List[str]], age: int) -> str:
    """
    Weave appropriate themes into the content
    """
    # This is a simplified approach - in practice, you'd use NLP to identify
    # insertion points and naturally weave in themes
    
    character_options = themes.get("characters", ["exploradores"])
    theme_options = themes.get("themes", ["aventura"])
    
    # Add thematic elements naturally
    if age <= 6:
        adapted = content + f" ¿Te imaginas siendo un pequeño {character_options[0]}?"
    else:
        adapted = content + f" Como los grandes {character_options[0]} de la historia..."
    
    return adapted

def get_family_interaction_style(family_profile: FamilyProfile) -> str:
    """
    Determine interaction style based on family composition
    """
    children = family_profile.children
    num_children = len(children)
    
    if num_children == 1:
        child = children[0]
        return f"individual_{child.gender}_{child.age}"
    elif num_children == 2:
        ages = [child.age for child in children]
        age_gap = max(ages) - min(ages)
        if age_gap <= 2:
            return "siblings_close"
        else:
            return "siblings_mixed"
    else:
        return "group_large"

def generate_personalized_greeting(family_profile: FamilyProfile) -> str:
    """
    Generate a personalized greeting based on family composition
    """
    children = family_profile.children
    num_children = len(children)
    
    if num_children == 1:
        child = children[0]
        age_group = "pequeño" if child.age <= 6 else "joven"
        gender_adj = "pequeña" if child.gender == "girl" and child.age <= 6 else age_group
        name_part = f" {child.name}" if child.name else ""
        
        return f"¡Hola{name_part}, {gender_adj} aventurer{'a' if child.gender == 'girl' else 'o'}! 🐭✨"
    
    elif num_children == 2:
        return "¡Hola pareja de exploradores! 🐭✨ ¡Qué equipo tan genial!"
    
    else:
        return f"¡Hola increíble pandilla de {num_children} aventureros! 🐭✨ ¡Menudo grupo de valientes!"

def suggest_age_appropriate_activities(location_type: str, children: List[Child], weather: str) -> List[str]:
    """
    Suggest activities based on location, ages, and weather
    """
    min_age = min(child.age for child in children)
    max_age = max(child.age for child in children)
    num_children = len(children)
    
    activities = []
    
    # Base activities by location
    location_activities = {
        "plaza": {
            "simple": ["contar ventanas", "buscar ratoncitos escondidos", "juego de las sombras"],
            "moderate": ["buscar escudos en los edificios", "inventar historias de las ventanas", "cazar tesoros históricos"],
            "advanced": ["detective de la historia", "arquitecto por un día", "cronista de leyendas"]
        },
        "palace": {
            "simple": ["contar torres", "imaginar princesas", "buscar puertas mágicas"],
            "moderate": ["explorar jardines reales", "crear cuentos de realeza", "buscar símbolos reales"],
            "advanced": ["historiador real", "diplomático de corte", "arqueólogo de palacio"]
        },
        "park": {
            "simple": ["buscar animales", "recoger hojas", "correr como el viento"],
            "moderate": ["exploración botánica", "circuito de aventura", "historias de árboles"],
            "advanced": ["naturalista urbano", "geólogo de parque", "biólogo de ciudad"]
        }
    }
    
    # Determine complexity level
    if max_age <= 6:
        complexity = "simple"
    elif max_age <= 9:
        complexity = "moderate"
    else:
        complexity = "advanced"
    
    # Get base activities
    base_activities = location_activities.get(location_type, location_activities["plaza"])[complexity]
    
    # Adapt for group size
    if num_children == 1:
        activities.extend([f"{activity} (solo)" for activity in base_activities[:2]])
    elif num_children <= 3:
        activities.extend([f"{activity} (en equipo)" for activity in base_activities])
    else:
        activities.extend([f"{activity} (gran grupo)" for activity in base_activities])
        activities.append("competición amistosa por equipos")
    
    # Weather adaptations
    if "lluvia" in weather.lower():
        activities = [activity.replace("correr", "caminar bajo techado") for activity in activities]
        activities.append("juego de historias de lluvia")
    
    return activities[:3]  # Limit to 3 activities
