from fastapi import APIRouter
from pydantic import BaseModel
import os
try:
    from crewai import Crew, Agent, Task
except Exception:
    # crewai is an optional dependency for enhanced educational responses.
    # If it's not installed we fall back to a safe behavior in the endpoint.
    Crew = None
    Agent = None
    Task = None

try:
    from langchain_groq import ChatGroq
except Exception:
    # langchain_groq (ChatGroq) is optional; if missing we'll set llm=None below
    ChatGroq = None

router = APIRouter()

class CrewAiExplainRequest(BaseModel):
    topic: str
    age: int
    correct_answer: str
    selected_place: str
    question: str

class CrewAiExplainResponse(BaseModel):
    reply: str


# Obtener y validar la API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Initialize LLM only if ChatGroq is available and an API key is configured
if not GROQ_API_KEY or ChatGroq is None:
    import logging
    if ChatGroq is None:
        logging.warning("langchain_groq.ChatGroq no disponible; las respuestas educativas avanzadas estarán deshabilitadas.")
    else:
        logging.error("GROQ_API_KEY no está configurada en el entorno. Por favor, añade tu clave al archivo .env.")
    llm = None
else:
    # Inicialización compatible con CrewAI/langchain_groq
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="groq/llama-3.1-8b-instant",
        temperature=0.4,
        max_tokens=800
    )

def build_prompt(topic: str, age: int, correct_answer: str, selected_place: str, question: str) -> str:
    """
    Construye un prompt personalizado y educativo para el LLM, integrando la respuesta correcta, el lugar seleccionado y la pregunta del juego.
    """
    if age < 6:
        return (
            f"Responde de forma muy sencilla y divertida para un niño de 3 a 5 años. "
            f"La pregunta del juego fue: '{question}'. "
            f"El lugar seleccionado es: {selected_place}. "
            f"La respuesta correcta es: {correct_answer}. "
            f"Explica por qué esa es la respuesta correcta y añade un dato curioso o educativo sobre {selected_place} relacionado con la pregunta. "
            f"Habla en singular, dirigiéndote solo al niño, usando frases cortas y ejemplos fáciles. No uses 'vosotros' ni 'ustedes'. Sé cálido y cercano. "
            f"Haz la explicación lo más breve y relevante posible, solo lo esencial para que el niño lo entienda fácilmente."
        )
    elif age <= 9:
        return (
            f"Responde de forma clara y curiosa para un niño de 6 a 9 años. "
            f"La pregunta del juego fue: '{question}'. "
            f"El lugar seleccionado es: {selected_place}. "
            f"La respuesta correcta es: {correct_answer}. "
            f"Explica por qué esa es la respuesta correcta y añade un dato interesante o educativo sobre {selected_place} relacionado con la pregunta. "
            f"Habla en singular, dirigiéndote solo al niño, y adapta el tono a su edad. No uses 'vosotros' ni 'ustedes'. "
            f"Haz la explicación lo más breve y relevante posible, solo lo esencial para que el niño lo entienda fácilmente."
        )
    else:
        return (
            f"Responde de forma educativa y entretenida para un niño de 10 a 12 años. "
            f"La pregunta del juego fue: '{question}'. "
            f"El lugar seleccionado es: {selected_place}. "
            f"La respuesta correcta es: {correct_answer}. "
            f"Explica por qué esa es la respuesta correcta y añade un dato curioso, histórico o educativo sobre {selected_place} relacionado con la pregunta. "
            f"Habla en singular, dirigiéndote solo al niño, y adapta el tono a su edad. No uses 'vosotros' ni 'ustedes'. "
            f"Haz la explicación lo más breve y relevante posible, solo lo esencial para que el niño lo entienda fácilmente."
        )


@router.post("/game/crew-explain", response_model=CrewAiExplainResponse)
async def crew_explain_agent(req: CrewAiExplainRequest):
    import logging
    if not llm:
        logging.error("No se pudo inicializar el LLM porque falta la API key.")
        return CrewAiExplainResponse(reply="No se pudo obtener respuesta educativa porque falta la configuración del LLM. Contacta con el administrador.")
    prompt = build_prompt(
        req.topic,
        req.age,
        req.correct_answer,
        req.selected_place,
        req.question
    )
    try:
        # Definir un agente CrewAI simple
        agent = Agent(
            role="Guía educativo",
            goal="Explicar temas culturales a niños de forma divertida y adaptada a su edad.",
            backstory="Eres un guía experto en arte y cultura para niños, siempre explicas de forma clara y entretenida.",
            llm=llm,
            verbose=False
        )
        task = Task(
            description=prompt,
            agent=agent,
            expected_output="Una explicación educativa, adaptada a la edad {age} del niño, sobre el tema solicitado."
        )
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        result = crew.kickoff()
        # CrewOutput puede tener .output o .result según versión
        reply_text = getattr(result, 'output', None) or getattr(result, 'result', None) or str(result)
        if not reply_text or not str(reply_text).strip():
            logging.warning(f"El LLM no devolvió respuesta para el prompt: {prompt}")
            return CrewAiExplainResponse(reply="No se pudo obtener respuesta educativa del agente. Intenta de nuevo más tarde.")
        # Filtrar razonamientos internos tipo 'Thought:'
        lines = str(reply_text).splitlines()
        filtered = [l for l in lines if not l.strip().lower().startswith('thought:') and l.strip()]
        reply_str = '\n'.join(filtered).strip()
        if not reply_str:
            reply_str = "No se pudo obtener una explicación educativa. Intenta de nuevo más tarde."
        return CrewAiExplainResponse(reply=reply_str)
    except Exception as e:
        logging.error(f"Error al generar explicación educativa: {e}")
        return CrewAiExplainResponse(reply="No se pudo obtener respuesta educativa por un error interno. Intenta de nuevo más tarde.")
