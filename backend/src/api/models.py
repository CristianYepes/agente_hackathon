# backend/src/api/models.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class Location(BaseModel):
    """Modelo para ubicaciones de Madrid"""
    latitude: float = Field(..., description="Latitud GPS")
    longitude: float = Field(..., description="Longitud GPS")
    name: Optional[str] = Field(None, description="Nombre del lugar")
    address: Optional[str] = Field(None, description="Dirección")
    category: Optional[str] = Field(None, description="Categoría del lugar")

class Child(BaseModel):
    """Información de un niño"""
    age: int = Field(..., description="Edad del niño", ge=0, le=18)
    gender: Optional[str] = Field(None, description="Género (opcional)")
    interests: List[str] = Field(default=[], description="Intereses del niño")

class FamilyProfile(BaseModel):
    """Perfil familiar para personalización"""
    children: List[Child] = Field(default=[], description="Lista de niños")
    children_ages: List[int] = Field(default=[], description="Edades de los niños")
    interests: List[str] = Field(default=[], description="Intereses familiares")
    accessibility_needs: Optional[str] = Field(None, description="Necesidades de accesibilidad")
    language_preference: str = Field(default="spanish", description="Idioma preferido")

class ChatRequest(BaseModel):
    """Solicitud de chat al Ratoncito Pérez"""
    message: str = Field(..., description="Mensaje del usuario")
    session_id: Optional[str] = Field(None, description="ID de sesión")
    user_id: Optional[str] = Field(None, description="ID del usuario")
    location: Optional[Location] = Field(None, description="Ubicación actual")
    family_profile: Optional[FamilyProfile] = Field(None, description="Perfil familiar")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Contexto adicional")

class ChatResponse(BaseModel):
    """Respuesta del Ratoncito Pérez"""
    message: str = Field(..., description="Respuesta del agente")
    session_id: Optional[str] = Field(None, description="ID de sesión")
    suggestions: List[str] = Field(default=[], description="Sugerencias de actividades")
    locations_suggested: List[Location] = Field(default=[], description="Lugares sugeridos")
    context_used: Optional[str] = Field(None, description="Contexto utilizado")
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    """Respuesta del health check"""
    status: str
    services: Dict[str, str]
    cors: str
    frontend_path: Optional[str] = None
