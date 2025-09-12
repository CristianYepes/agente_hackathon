# backend/src/api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Cargar variables de entorno
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path)

from .models import ChatRequest, ChatResponse, Location, FamilyProfile, HealthResponse

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="Ratoncito Pérez - Guía Mágico de Madrid",
    description="API del agente narrativo del Ratoncito Pérez para familias visitando Madrid",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos del frontend
frontend_build_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "build")
if os.path.exists(frontend_build_path):
    app.mount("/static", StaticFiles(directory=frontend_build_path), name="static")

@app.get("/")
async def root():
    """Servir frontend o información de la API"""
    frontend_index = os.path.join(frontend_build_path, "index.html")
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index)

    return {
        "message": "¡Hola! Soy el Ratoncito Pérez 🐭✨",
        "status": "active",
        "version": "1.0.0",
        "frontend": "Frontend not found - run 'npm run build' in frontend/",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "locations": "/madrid-locations",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        from src.langgraph.narrative_flow import narrative_graph
        graph_status = "active"
    except Exception as e:
        logger.error(f"Graph import error: {e}")
        graph_status = f"error: {str(e)}"

    groq_configured = bool(os.getenv("GROQ_API_KEY"))
    weather_configured = bool(os.getenv("OPENWEATHER_API_KEY"))

    return HealthResponse(
        status="healthy",
        services={
            "groq_llm": "configured" if groq_configured else "using_mock",
            "weather_api": "configured" if weather_configured else "using_mock",
            "location_service": "active",
            "narrative_engine": graph_status
        },
        cors="enabled",
        frontend_path=frontend_build_path if os.path.exists(frontend_build_path) else None
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ratoncito(request: ChatRequest):
    """Endpoint principal del chat con el Ratoncito Pérez"""
    try:
        # Importar aquí para evitar imports circulares
        from src.langgraph.narrative_flow import narrative_graph

        # Generar session_id si no existe
        session_id = request.session_id or str(uuid.uuid4())

        # Configurar para LangGraph
        config = {
            "configurable": {
                "thread_id": session_id,
                "user_id": request.user_id or "anonymous"
            }
        }

        # Preparar el estado inicial
        initial_state = {
            "user_message": request.message,
            "current_step": "start",
            "user_location": request.location.dict() if request.location else None,
            "family_profile": request.family_profile.dict() if request.family_profile else None,
            "context_info": request.context,
            "session_id": session_id
        }

        # Invocar el grafo de LangGraph
        logger.info(f"Processing message: {request.message[:50]}...")
        result = await narrative_graph.ainvoke(initial_state, config=config)

        # Extraer respuesta
        response_message = result.get("magical_response", "¡Hola! Soy el Ratoncito Pérez. ¿En qué puedo ayudarte? 🐭✨")

        return ChatResponse(
            message=response_message,
            session_id=session_id,
            suggestions=result.get("suggested_activities", []),
            locations_suggested=[],  # TODO: mapear ubicaciones sugeridas
            context_used=str(result.get("context_info", "")),
            timestamp=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando mensaje: {str(e)}"
        )

@app.get("/madrid-locations")
async def get_madrid_locations():
    """Obtener ubicaciones principales de Madrid"""
    locations = [
        Location(
            latitude=40.4170,
            longitude=-3.7032,
            name="Puerta del Sol",
            address="Puerta del Sol, 28013 Madrid",
            category="historico"
        ),
        Location(
            latitude=40.4152,
            longitude=-3.6844,
            name="Parque del Retiro",
            address="Plaza de la Independencia, 7, 28001 Madrid",
            category="parque"
        ),
        Location(
            latitude=40.4238,
            longitude=-3.6921,
            name="Museo del Prado",
            address="Calle de Ruiz de Alarcón, 23, 28014 Madrid",
            category="museo"
        ),
        Location(
            latitude=40.4200,
            longitude=-3.7088,
            name="Palacio Real",
            address="Calle de Bailén, s/n, 28071 Madrid",
            category="historico"
        )
    ]
    return locations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
