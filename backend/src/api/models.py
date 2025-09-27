from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Location(BaseModel):
    """GPS coordinates and detected location"""
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    place_name: Optional[str] = Field(None, description="Detected place name")

class Child(BaseModel):
    """Individual child profile"""
    age: int = Field(..., ge=3, le=12, description="Child age between 3-12")
    gender: str = Field(..., description="Child gender: 'boy', 'girl', or 'other'")
    name: Optional[str] = Field(None, description="Child's name (optional)")

class FamilyProfile(BaseModel):
    """Family composition and preferences"""
    children: List[Child] = Field(..., description="List of children in the family")
    language: str = Field(default="es", description="Preferred language")
    interests: List[str] = Field(default=[], description="Family interests")

class ChatRequest(BaseModel):
    """Request for chat interaction"""
    message: str = Field(..., description="User message or question")
    location: Location = Field(..., description="Current GPS location")
    family_profile: FamilyProfile = Field(..., description="Family composition")

class ChatResponse(BaseModel):
    """Response from Ratoncito Pérez"""
    response: str = Field(..., description="Main response from Ratoncito Pérez")
    activities: List[str] = Field(default=[], description="Suggested activities")
    suggestions: List[str] = Field(default=[], description="Follow-up questions")
    location_context: str = Field(..., description="Brief location context")

class NarrativeState(BaseModel):
    """Internal state for LangGraph processing"""
    location: Location
    family_profile: FamilyProfile
    user_message: str
    detected_place: Optional[str] = None
    weather_context: Optional[Dict] = None
    historical_context: Optional[str] = None
    adapted_content: Optional[str] = None
    final_response: Optional[str] = None
