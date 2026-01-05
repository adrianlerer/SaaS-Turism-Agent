"""
Map and location-related tools
Simulates functionality similar to STAgent's map tools
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import httpx
import asyncio
from .base import BaseTool, ToolInput, ToolOutput


class SearchPlacesInput(ToolInput):
    """Input for searching places"""
    query: str = Field(..., description="Search query for places")
    location: Optional[str] = Field(None, description="Center location (lat,lng)")
    radius: Optional[int] = Field(5000, description="Search radius in meters")
    type: Optional[str] = Field(None, description="Place type (restaurant, hotel, etc)")


class MapSearchPlacesTool(BaseTool):
    """Search for places of interest"""
    
    name = "map_search_places"
    description = "Search for places, points of interest, restaurants, hotels, attractions based on query and location"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key
    
    async def execute(self, input_data: SearchPlacesInput) -> ToolOutput:
        """Execute place search"""
        try:
            # Simulate Google Places API call
            # In production, use real API
            places = await self._search_places(
                input_data.query,
                input_data.location,
                input_data.radius,
                input_data.type
            )
            
            return ToolOutput(
                success=True,
                data=places,
                metadata={"count": len(places), "query": input_data.query}
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    async def _search_places(
        self, 
        query: str, 
        location: Optional[str], 
        radius: int,
        place_type: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Search places using external API"""
        # Simulated response - replace with actual API call
        await asyncio.sleep(0.1)  # Simulate API latency
        
        # Mock data
        mock_places = [
            {
                "id": "poi_001",
                "name": f"Sample {query} Place 1",
                "type": place_type or "attraction",
                "rating": 4.5,
                "reviews_count": 1234,
                "location": {"lat": 35.6762, "lng": 139.6503},
                "address": "Sample Address 1",
                "opening_hours": {"open_now": True},
                "price_level": 2,
                "description": f"A great place for {query}"
            },
            {
                "id": "poi_002",
                "name": f"Sample {query} Place 2",
                "type": place_type or "restaurant",
                "rating": 4.7,
                "reviews_count": 567,
                "location": {"lat": 35.6812, "lng": 139.7671},
                "address": "Sample Address 2",
                "opening_hours": {"open_now": True},
                "price_level": 3,
                "description": f"Popular spot for {query}"
            }
        ]
        
        return mock_places
    
    def get_input_schema(self) -> Dict[str, Any]:
        return SearchPlacesInput.model_json_schema()


class ComputeRouteInput(ToolInput):
    """Input for route computation"""
    origin: str = Field(..., description="Starting location (address or lat,lng)")
    destination: str = Field(..., description="Destination location")
    mode: str = Field("driving", description="Travel mode: driving, walking, transit, bicycling")
    waypoints: Optional[List[str]] = Field(None, description="Intermediate waypoints")


class MapComputeRoutesTool(BaseTool):
    """Compute routes between locations"""
    
    name = "map_compute_routes"
    description = "Calculate routes between locations with different travel modes, including distance, duration, and steps"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key
    
    async def execute(self, input_data: ComputeRouteInput) -> ToolOutput:
        """Execute route computation"""
        try:
            route = await self._compute_route(
                input_data.origin,
                input_data.destination,
                input_data.mode,
                input_data.waypoints
            )
            
            return ToolOutput(
                success=True,
                data=route,
                metadata={"mode": input_data.mode}
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    async def _compute_route(
        self,
        origin: str,
        destination: str,
        mode: str,
        waypoints: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Compute route using external API"""
        await asyncio.sleep(0.1)
        
        # Mock route data
        duration_map = {
            "walking": 3600,
            "driving": 1200,
            "transit": 1800,
            "bicycling": 2400
        }
        
        distance_map = {
            "walking": 5000,
            "driving": 15000,
            "transit": 12000,
            "bicycling": 8000
        }
        
        return {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "distance_meters": distance_map.get(mode, 10000),
            "duration_seconds": duration_map.get(mode, 1800),
            "steps": [
                {
                    "instruction": "Head northeast on Main St",
                    "distance": 500,
                    "duration": 120
                },
                {
                    "instruction": "Turn right onto 2nd Ave",
                    "distance": 1200,
                    "duration": 300
                }
            ],
            "polyline": "encoded_polyline_data",
            "waypoints": waypoints or []
        }
    
    def get_input_schema(self) -> Dict[str, Any]:
        return ComputeRouteInput.model_json_schema()


class SearchAlongRouteInput(ToolInput):
    """Input for searching places along a route"""
    origin: str = Field(..., description="Route origin")
    destination: str = Field(..., description="Route destination")
    query: str = Field(..., description="What to search for")
    max_detour_minutes: Optional[int] = Field(15, description="Maximum detour time")


class MapSearchAlongRouteTool(BaseTool):
    """Search for places along a route"""
    
    name = "map_search_along_route"
    description = "Find places of interest along a travel route without significant detour"
    
    async def execute(self, input_data: SearchAlongRouteInput) -> ToolOutput:
        """Execute search along route"""
        try:
            places = await self._search_along_route(
                input_data.origin,
                input_data.destination,
                input_data.query,
                input_data.max_detour_minutes
            )
            
            return ToolOutput(
                success=True,
                data=places,
                metadata={"query": input_data.query}
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    async def _search_along_route(
        self,
        origin: str,
        destination: str,
        query: str,
        max_detour: int
    ) -> List[Dict[str, Any]]:
        """Search places along route"""
        await asyncio.sleep(0.1)
        
        return [
            {
                "id": "poi_along_001",
                "name": f"{query} Along Route",
                "location": {"lat": 35.6895, "lng": 139.6917},
                "detour_minutes": 5,
                "distance_from_route_meters": 500,
                "rating": 4.3
            }
        ]
    
    def get_input_schema(self) -> Dict[str, Any]:
        return SearchAlongRouteInput.model_json_schema()


class SearchCentralPlacesInput(ToolInput):
    """Input for finding central meeting places"""
    locations: List[str] = Field(..., description="List of locations to find center for")
    place_type: Optional[str] = Field(None, description="Type of place to find")


class MapSearchCentralPlacesTool(BaseTool):
    """Find central places between multiple locations"""
    
    name = "map_search_central_places"
    description = "Find central meeting points equidistant from multiple locations"
    
    async def execute(self, input_data: SearchCentralPlacesInput) -> ToolOutput:
        """Execute central place search"""
        try:
            places = await self._find_central_places(
                input_data.locations,
                input_data.place_type
            )
            
            return ToolOutput(
                success=True,
                data=places,
                metadata={"location_count": len(input_data.locations)}
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    async def _find_central_places(
        self,
        locations: List[str],
        place_type: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Find central places"""
        await asyncio.sleep(0.1)
        
        return [
            {
                "id": "poi_central_001",
                "name": "Central Meeting Point",
                "location": {"lat": 35.6850, "lng": 139.7514},
                "total_distance_meters": 5000,
                "max_distance_meters": 2000,
                "type": place_type or "cafe",
                "rating": 4.6
            }
        ]
    
    def get_input_schema(self) -> Dict[str, Any]:
        return SearchCentralPlacesInput.model_json_schema()
