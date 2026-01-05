"""
Pydantic schemas for travel plans
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date


class TravelConstraints(BaseModel):
    """Travel plan constraints"""
    duration_days: Optional[int] = Field(3, description="Number of days")
    budget_usd: Optional[float] = Field(1000, description="Budget in USD")
    travelers: Optional[int] = Field(1, description="Number of travelers")
    interests: Optional[List[str]] = Field(default_factory=list, description="Interests")
    destination: Optional[str] = Field(None, description="Destination")
    origin: Optional[str] = Field(None, description="Origin city")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    transport_mode: Optional[str] = Field("walking", description="Preferred transport")
    needs_flight: Optional[bool] = Field(False, description="Need flight booking")


class PlanRequest(BaseModel):
    """Request to create a travel plan"""
    query: str = Field(..., description="Natural language travel planning query")
    constraints: Optional[TravelConstraints] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "Plan a 3-day trip to Tokyo for 2 people interested in culture and food",
                "constraints": {
                    "duration_days": 3,
                    "budget_usd": 2000,
                    "travelers": 2,
                    "interests": ["culture", "food"],
                    "destination": "Tokyo"
                }
            }
        }
    }


class PlanResponse(BaseModel):
    """Response containing travel plan"""
    plan_id: str = Field(..., description="Unique plan ID")
    status: str = Field(..., description="Plan status")
    itinerary: Dict[str, Any] = Field(..., description="Generated itinerary")
    reasoning_trace: List[Dict[str, Any]] = Field(default_factory=list, description="Agent reasoning steps")
    confidence_score: float = Field(0.8, description="Confidence in plan quality")
    execution_time_ms: float = Field(0, description="Execution time in milliseconds")
