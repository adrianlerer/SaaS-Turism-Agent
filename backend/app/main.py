"""
TravelAgent Pro - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict, Any
import time

from .core.config import settings
from .tools.map_tools import (
    MapSearchPlacesTool,
    MapComputeRoutesTool,
    MapSearchAlongRouteTool,
    MapSearchCentralPlacesTool
)
from .tools.travel_tools import (
    TravelSearchFlightsTool,
    TravelSearchTrainsTool
)
from .agents.travel_planner import TravelPlannerAgent
from .schemas.plans import PlanRequest, PlanResponse


# Lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"📍 API Docs: http://localhost:8000/docs")
    yield
    # Shutdown
    print("👋 Shutting down TravelAgent Pro")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Agentic Travel Planning SaaS",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize tools
def get_tools():
    """Initialize all tools"""
    return [
        MapSearchPlacesTool(api_key=settings.GOOGLE_MAPS_API_KEY),
        MapComputeRoutesTool(api_key=settings.GOOGLE_MAPS_API_KEY),
        MapSearchAlongRouteTool(),
        MapSearchCentralPlacesTool(),
        TravelSearchFlightsTool(),
        TravelSearchTrainsTool()
    ]


# Initialize agent
def get_agent():
    """Get travel planner agent"""
    tools = get_tools()
    return TravelPlannerAgent(
        tools=tools,
        max_iterations=settings.MAX_ITERATIONS
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "docs": "/docs",
        "api": settings.API_V1_PREFIX
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


@app.post(f"{settings.API_V1_PREFIX}/plans", response_model=PlanResponse)
async def create_travel_plan(
    request: PlanRequest,
    agent: TravelPlannerAgent = Depends(get_agent)
):
    """
    Create a travel plan using AI agent
    
    This endpoint uses an agentic AI system to:
    - Discover relevant POIs
    - Search for flights/trains
    - Compute optimal routes
    - Generate day-by-day itineraries
    """
    try:
        # Run agent
        trace = await agent.run(
            query=request.query,
            context=request.constraints.model_dump() if request.constraints else {}
        )
        
        if not trace.success:
            raise HTTPException(
                status_code=500,
                detail=f"Agent failed: {trace.error}"
            )
        
        # Parse itinerary from trace
        import json
        itinerary = json.loads(trace.final_answer)
        
        return PlanResponse(
            plan_id=itinerary["id"],
            status="completed",
            itinerary=itinerary,
            reasoning_trace=[t.model_dump() for t in trace.thoughts],
            confidence_score=itinerary.get("confidence_score", 0.8),
            execution_time_ms=trace.execution_time_ms
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create plan: {str(e)}"
        )


@app.get(f"{settings.API_V1_PREFIX}/plans/{{plan_id}}")
async def get_travel_plan(plan_id: str):
    """Get existing travel plan"""
    # In production, fetch from database
    return {
        "plan_id": plan_id,
        "status": "completed",
        "message": "Plan retrieval from database not yet implemented"
    }


@app.get(f"{settings.API_V1_PREFIX}/tools")
async def list_tools():
    """List available tools"""
    tools = get_tools()
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in tools
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
