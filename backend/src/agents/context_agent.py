import os
import logging
from typing import Dict, Any
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)

class ContextRetrievalAgent:
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
            temperature=0.4,
            max_tokens=800
        )

    def research_location_context(self, location_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            place_name = location_data.get("place_name", "Madrid")
            place_type = location_data.get("place_type", "location")

            logger.info(f"🔍 Researching context for: {place_name}")

            historical_info = self._get_historical_context(place_name, place_type)
            cultural_context = self._get_cultural_context(place_name)
            legends_stories = self._get_legends_and_stories(place_name)
            educational_content = self._get_educational_content(place_name, place_type)

            result = {
                "historical_facts": historical_info,
                "cultural_significance": cultural_context,
                "legends_and_stories": legends_stories,
                "educational_content": educational_content,
                "fun_facts": self._get_fun_facts(place_name),
                "family_learning_opportunities": self._get_learning_opportunities(place_name, place_type)
            }

            logger.info(f"✅ Context research completed for {place_name}")
            return result

        except Exception as e:
            logger.error(f"❌ Error in context research: {e}")
            return self._create_fallback_context(location_data)

    def _get_historical_context(self, place_name: str, place_type: str) -> list:
        if self.llm:
            return self._get_llm_historical_context(place_name, place_type)
        else:
            return self._get_mock_historical_context(place_name)

    def _get_llm_historical_context(self, place_name: str, place_type: str) -> list:
        try:
            prompt = f"""Proporciona 3-4 datos históricos fascinantes sobre {place_name} en Madrid.

Tipo de lugar: {place_type}

Enfócate en:
- Hechos históricos verificables
- Información apropiada para familias con niños
- Datos que despierten curiosidad
- Fechas y eventos importantes

Formato: Lista de hechos concisos, cada uno en una línea separada.
Máximo 60 palabras por hecho."""

            response = self.llm.invoke(prompt)
            facts = [fact.strip() for fact in response.content.split('\n') if fact.strip() and not fact.strip().startswith('-')]
            return facts[:4]

        except Exception as e:
            logger.error(f"Error getting LLM historical context: {e}")
            return self._get_mock_historical_context(place_name)

    def _get_mock_historical_context(self, place_name: str) -> list:
        historical_data = {
            "Plaza Mayor": [
                "Construida entre 1617 y 1619 durante el reinado de Felipe III",
                "Originally llamada Plaza del Arrabal, cambió de nombre varias veces",
                "Ha sobrevivido a tres grandes incendios a lo largo de su historia",
                "Fue el centro de celebraciones reales, corridas de toros y ejecuciones públicas"
            ],
            "Palacio Real": [
                "Construido sobre las ruinas del antiguo Alcázar que se quemó en 1734",
                "Tiene más de 3.000 habitaciones, siendo uno de los palacios más grandes de Europa",
                "Su construcción duró 26 años, desde 1738 hasta 1764",
                "Guarda la colección de instrumentos musicales Stradivarius más importante del mundo"
            ],
            "Puerta del Sol": [
                "Es el kilómetro cero de las carreteras radiales españolas desde 1950",
                "Su nombre proviene de un sol que decoraba la entrada de un castillo que había aquí",
                "Aquí están las famosas campanadas de Año Nuevo que ve toda España",
                "La Casa de Correos, construida en 1768, es el edificio más emblemático"
            ],
            "Parque del Retiro": [
                "Creado en el siglo XVII como jardín real para Felipe IV",
                "Abrió al público en 1868 tras la Revolución de 1868",
                "Tiene 125 hectáreas y más de 15.000 árboles",
                "El Palacio de Cristal fue construido en 1887 para una exposición de Filipinas"
            ]
        }

        return historical_data.get(place_name, [
            f"{place_name} tiene una rica historia que se remonta a varios siglos",
            "Este lugar ha sido testigo de importantes eventos en la historia de Madrid",
            "Ha evolucionado a lo largo del tiempo manteniendo su carácter especial",
            "Forma parte del patrimonio histórico y cultural de Madrid"
        ])

    def _get_cultural_context(self, place_name: str) -> str:
        cultural_significance = {
            "Plaza Mayor": "Símbolo del Madrid de los Austrias y corazón social de la ciudad. Representa la España imperial y es un ejemplo perfecto de la arquitectura barroca española.",
            "Palacio Real": "Representa la monarquía española y es símbolo del poder real. Su arquitectura italiana marca la transición del barroco al neoclásico en España.",
            "Puerta del Sol": "Centro neurálgico de Madrid y punto de referencia nacional. Simboliza la unión de España al ser el kilómetro cero de todas las carreteras.",
            "Parque del Retiro": "Pulmón verde de Madrid que representa el equilibrio entre naturaleza y ciudad. Simboliza la democratización de los espacios reales para el pueblo.",
            "Plaza de Cibeles": "Icono de Madrid que representa la conexión con la mitología clásica y el poder municipal de la ciudad."
        }

        return cultural_significance.get(place_name, f"{place_name} es una parte importante del patrimonio cultural de Madrid, representando la rica historia y tradiciones de la ciudad.")

    def _get_legends_and_stories(self, place_name: str) -> list:
        legends = {
            "Plaza Mayor": [
                "Se dice que en las noches de luna llena, se pueden escuchar los ecos de las antiguas celebraciones reales",
                "La leyenda cuenta que Felipe III ordenó construir la plaza tras soñar con un gran espacio donde todo Madrid pudiera reunirse",
                "Los vecinos cuentan que cada ventana de la plaza tiene una historia diferente que contar"
            ],
            "Palacio Real": [
                "Se rumorea que los fantasmas de antiguos reyes aún pasean por sus pasillos durante las noches",
                "La leyenda dice que en la sala del trono se escuchan susurros de decisiones que cambiaron la historia de España",
                "Cuenta la historia que los gatos del palacio son descendientes de los felinos favoritos de la realeza"
            ],
            "Puerta del Sol": [
                "La tradición dice que quien pise el kilómetro cero y pida un deseo, regresará a Madrid",
                "Se cuenta que el oso y el madroño fueron elegidos como símbolos tras una antigua leyenda medieval",
                "La leyenda urbana dice que las campanadas de Año Nuevo tienen poderes mágicos para cumplir deseos"
            ],
            "Parque del Retiro": [
                "Se dice que las ardillas del Retiro son descendientes de las mascotas reales",
                "La leyenda cuenta que el Palacio de Cristal fue construido con cristales mágicos que reflejan sueños",
                "Los madrileños creen que hacer un picnic bajo ciertos árboles trae buena suerte a las familias"
            ]
        }

        return legends.get(place_name, [
            f"Las leyendas de {place_name} hablan de su importancia especial en la historia de Madrid",
            "Los vecinos del barrio guardan historias tradicionales sobre este lugar",
            "Se dice que este lugar tiene una energía especial que atrae a las familias"
        ])

    def _get_educational_content(self, place_name: str, place_type: str) -> Dict[str, Any]:
        return {
            "key_concepts": self._get_key_learning_concepts(place_name, place_type),
            "age_appropriate_facts": self._get_age_appropriate_facts(place_name),
            "interactive_questions": self._get_interactive_questions(place_name),
            "connections_to_curriculum": self._get_curriculum_connections(place_type)
        }

    def _get_key_learning_concepts(self, place_name: str, place_type: str) -> list:
        concepts_map = {
            "plaza": ["Arquitectura barroca", "Vida social histórica", "Urbanismo español", "Historia de Madrid"],
            "palace": ["Monarquía española", "Arquitectura neoclásica", "Arte y decoración", "Protocolo real"],
            "park": ["Jardinería histórica", "Biodiversidad urbana", "Espacios públicos", "Recreación familiar"],
            "museum": ["Arte y cultura", "Historia española", "Conservación patrimonial", "Educación cultural"]
        }

        return concepts_map.get(place_type, ["Historia de Madrid", "Patrimonio cultural", "Arquitectura española", "Tradiciones madrileñas"])

    def _get_age_appropriate_facts(self, place_name: str) -> Dict[str, list]:
        return {
            "3-6_años": [
                f"{place_name} es muy grande y muy bonito",
                "Aquí vivían personas importantes hace mucho tiempo",
                "Podemos ver cosas muy antiguas y especiales"
            ],
            "7-10_años": [
                f"{place_name} se construyó hace cientos de años",
                "Era un lugar muy importante para los reyes y la gente de Madrid",
                "Tiene historias emocionantes sobre el pasado de nuestra ciudad"
            ],
            "11-12_años": [
                f"{place_name} representa un período histórico específico de España",
                "Su arquitectura refleja las influencias culturales de diferentes épocas",
                "Ha sido testigo de eventos históricos que definieron la identidad madrileña"
            ]
        }

    def _get_interactive_questions(self, place_name: str) -> list:
        return [
            f"¿Qué detalles especiales puedes observar en {place_name}?",
            "¿Cómo crees que era la vida aquí hace 300 años?",
            "¿Qué diferencias ves entre este lugar y los edificios modernos?",
            "¿Por qué crees que este lugar es importante para Madrid?",
            "¿Qué historia inventarías sobre este lugar?"
        ]

    def _get_curriculum_connections(self, place_type: str) -> list:
        connections = {
            "plaza": ["Historia de España", "Geografía urbana", "Arte y arquitectura"],
            "palace": ["Historia de la monarquía", "Arte barroco/neoclásico", "Ciencias sociales"],
            "park": ["Ciencias naturales", "Ecología urbana", "Educación ambiental"],
            "museum": ["Historia del arte", "Patrimonio cultural", "Historia contemporánea"]
        }

        return connections.get(place_type, ["Historia de Madrid", "Patrimonio cultural", "Educación cívica"])

    def _get_fun_facts(self, place_name: str) -> list:
        fun_facts = {
            "Plaza Mayor": [
                "Tiene exactamente 237 balcones con vista a la plaza",
                "Puede albergar hasta 50.000 personas en eventos especiales",
                "Se han rodado más de 100 películas en esta plaza"
            ],
            "Palacio Real": [
                "Tiene más habitaciones que el Palacio de Versalles",
                "Sus jardines tienen plantas de los cinco continentes",
                "Guarda 5.000 relojes antiguos en funcionamiento"
            ],
            "Puerta del Sol": [
                "Es más famosa por su reloj que por su arquitectura",
                "El oso y el madroño pesan más de 20 toneladas",
                "Más de 10 millones de personas pasan por aquí cada año"
            ]
        }

        return fun_facts.get(place_name, [
            f"{place_name} esconde secretos fascinantes en cada rincón",
            "Los arquitectos incluyeron detalles sorprendentes que pocos conocen",
            "Este lugar tiene récords únicos que lo hacen especial"
        ])

    def _get_learning_opportunities(self, place_name: str, place_type: str) -> list:
        return [
            "Observación arquitectónica detallada",
            "Comprensión de períodos históricos",
            "Desarrollo de la curiosidad cultural",
            "Apreciación del patrimonio español",
            "Conexión entre pasado y presente",
            "Estimulación de la imaginación histórica"
        ]

    def _create_fallback_context(self, location_data: Dict[str, Any]) -> Dict[str, Any]:
        place_name = location_data.get("place_name", "Madrid")

        return {
            "historical_facts": [
                f"{place_name} forma parte de la rica historia de Madrid",
                "Este lugar ha sido testigo de importantes eventos históricos",
                "Su arquitectura refleja diferentes épocas de la ciudad"
            ],
            "cultural_significance": f"{place_name} es una parte valiosa del patrimonio cultural madrileño",
            "legends_and_stories": [
                f"Las leyendas locales hacen de {place_name} un lugar especial",
                "Los madrileños guardan historias tradicionales sobre este sitio"
            ],
            "educational_content": {
                "key_concepts": ["Historia de Madrid", "Patrimonio cultural"],
                "age_appropriate_facts": {
                    "3-6_años": ["Es un lugar muy especial en Madrid"],
                    "7-10_años": ["Tiene una historia interesante que contar"],
                    "11-12_años": ["Representa el patrimonio histórico de nuestra ciudad"]
                },
                "interactive_questions": [
                    "¿Qué te parece más interesante de este lugar?",
                    "¿Cómo imaginas que era hace mucho tiempo?"
                ],
                "connections_to_curriculum": ["Historia", "Ciencias sociales"]
            },
            "fun_facts": [f"{place_name} tiene secretos fascinantes por descubrir"],
            "family_learning_opportunities": [
                "Exploración histórica en familia",
                "Desarrollo de la curiosidad cultural"
            ]
        }

context_agent = ContextRetrievalAgent()
