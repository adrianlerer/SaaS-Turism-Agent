"""
Travel booking tools (flights, trains)
"""
from typing import List, Optional, Dict, Any
from pydantic import Field
from datetime import datetime, date
import asyncio
from .base import BaseTool, ToolInput, ToolOutput


class SearchFlightsInput(ToolInput):
    """Input for flight search"""
    origin: str = Field(..., description="Departure airport code")
    destination: str = Field(..., description="Arrival airport code")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(None, description="Return date for round trip")
    passengers: int = Field(1, description="Number of passengers")
    class_type: str = Field("economy", description="Cabin class")


class TravelSearchFlightsTool(BaseTool):
    """Search for flights"""
    
    name = "travel_search_flights"
    description = "Search for flights between cities with dates, prices, and availability"
    
    async def execute(self, input_data: SearchFlightsInput) -> ToolOutput:
        """Execute flight search"""
        try:
            flights = await self._search_flights(
                input_data.origin,
                input_data.destination,
                input_data.departure_date,
                input_data.return_date,
                input_data.passengers,
                input_data.class_type
            )
            
            return ToolOutput(
                success=True,
                data=flights,
                metadata={"result_count": len(flights)}
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    async def _search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str],
        passengers: int,
        class_type: str
    ) -> List[Dict[str, Any]]:
        """Search flights via API"""
        await asyncio.sleep(0.15)
        
        return [
            {
                "flight_id": "FL001",
                "airline": "Sample Airlines",
                "flight_number": "SA123",
                "origin": origin,
                "destination": destination,
                "departure": {
                    "date": departure_date,
                    "time": "10:00",
                    "airport": origin
                },
                "arrival": {
                    "date": departure_date,
                    "time": "14:30",
                    "airport": destination
                },
                "duration_minutes": 270,
                "price_usd": 450,
                "currency": "USD",
                "class": class_type,
                "stops": 0,
                "available_seats": 15
            },
            {
                "flight_id": "FL002",
                "airline": "Budget Air",
                "flight_number": "BA456",
                "origin": origin,
                "destination": destination,
                "departure": {
                    "date": departure_date,
                    "time": "15:30",
                    "airport": origin
                },
                "arrival": {
                    "date": departure_date,
                    "time": "20:15",
                    "airport": destination
                },
                "duration_minutes": 285,
                "price_usd": 320,
                "currency": "USD",
                "class": class_type,
                "stops": 1,
                "available_seats": 8
            }
        ]
    
    def get_input_schema(self) -> Dict[str, Any]:
        return SearchFlightsInput.model_json_schema()


class SearchTrainsInput(ToolInput):
    """Input for train search"""
    origin: str = Field(..., description="Departure station")
    destination: str = Field(..., description="Arrival station")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    passengers: int = Field(1, description="Number of passengers")


class TravelSearchTrainsTool(BaseTool):
    """Search for trains"""
    
    name = "travel_search_trains"
    description = "Search for train connections between cities"
    
    async def execute(self, input_data: SearchTrainsInput) -> ToolOutput:
        """Execute train search"""
        try:
            trains = await self._search_trains(
                input_data.origin,
                input_data.destination,
                input_data.departure_date,
                input_data.passengers
            )
            
            return ToolOutput(
                success=True,
                data=trains,
                metadata={"result_count": len(trains)}
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    async def _search_trains(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        passengers: int
    ) -> List[Dict[str, Any]]:
        """Search trains via API"""
        await asyncio.sleep(0.12)
        
        return [
            {
                "train_id": "TR001",
                "operator": "Express Rail",
                "train_number": "ER789",
                "origin": origin,
                "destination": destination,
                "departure": {
                    "date": departure_date,
                    "time": "09:15",
                    "station": origin
                },
                "arrival": {
                    "date": departure_date,
                    "time": "11:45",
                    "station": destination
                },
                "duration_minutes": 150,
                "price_usd": 85,
                "currency": "USD",
                "class": "standard",
                "available_seats": 42
            }
        ]
    
    def get_input_schema(self) -> Dict[str, Any]:
        return SearchTrainsInput.model_json_schema()
