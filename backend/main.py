# backend/main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import os

app = FastAPI()

class HealthResponse(BaseModel):
    status: str
    services: dict
    cors: str
    frontend_path: str | None

@app.get("/health", response_model=HealthResponse)
async def health_check(use_mock: bool = False):
    # Merge logic from both versions
    try:
        if not use_mock:
            from src.langgraph.narrative_flow import narrative_graph
            graph_status = "active"
        else:
            graph_status = "using_mock"
    except Exception as e:
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
