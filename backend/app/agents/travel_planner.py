"""
Travel Planning Agent
Main agentic planner inspired by STAgent
"""
from typing import Dict, Any, Optional, List
import json
import time
from .base_agent import BaseAgent, AgentTrace, AgentThought


class TravelPlannerAgent(BaseAgent):
    """
    Main travel planning agent that uses tool calling
    to discover POIs, plan routes, and create itineraries
    """
    
    def __init__(self, tools: List[Any], llm_client=None, max_iterations: int = 10):
        super().__init__(
            name="TravelPlanner",
            description="AI agent for travel planning and itinerary generation",
            tools=tools,
            max_iterations=max_iterations
        )
        self.llm_client = llm_client
    
    async def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentTrace:
        """
        Run the travel planner agent
        Implements ReAct-style reasoning: Thought -> Action -> Observation
        """
        start_time = time.time()
        trace = AgentTrace()
        context = context or {}
        
        try:
            # Parse query to extract constraints
            constraints = self._parse_constraints(query, context)
            
            # Step 1: Discover POIs
            step = 1
            thought = AgentThought(
                step=step,
                thought=f"I need to find places of interest for: {constraints.get('interests', [])}",
                tool_name="map_search_places",
                tool_input={"query": query, "location": constraints.get("location")}
            )
            
            poi_output = await self.execute_tool(
                "map_search_places",
                thought.tool_input
            )
            thought.tool_output = poi_output
            trace.thoughts.append(thought)
            
            if not self.verify_output(poi_output):
                trace.error = "Failed to discover POIs"
                trace.success = False
                return trace
            
            pois = poi_output.get("data", [])
            
            # Step 2: Search for flights if needed
            if constraints.get("needs_flight"):
                step += 1
                thought = AgentThought(
                    step=step,
                    thought="Searching for flights to destination",
                    tool_name="travel_search_flights",
                    tool_input={
                        "origin": constraints.get("origin"),
                        "destination": constraints.get("destination"),
                        "departure_date": constraints.get("start_date"),
                        "passengers": constraints.get("travelers", 1)
                    }
                )
                
                flight_output = await self.execute_tool(
                    "travel_search_flights",
                    thought.tool_input
                )
                thought.tool_output = flight_output
                trace.thoughts.append(thought)
            
            # Step 3: Compute routes between POIs
            if len(pois) >= 2:
                step += 1
                thought = AgentThought(
                    step=step,
                    thought="Computing optimal route between points of interest",
                    tool_name="map_compute_routes",
                    tool_input={
                        "origin": pois[0].get("address", ""),
                        "destination": pois[-1].get("address", ""),
                        "mode": constraints.get("transport_mode", "walking")
                    }
                )
                
                route_output = await self.execute_tool(
                    "map_compute_routes",
                    thought.tool_input
                )
                thought.tool_output = route_output
                trace.thoughts.append(thought)
            
            # Step 4: Generate final itinerary
            step += 1
            itinerary = self._generate_itinerary(
                pois=pois,
                constraints=constraints,
                trace=trace
            )
            
            final_thought = AgentThought(
                step=step,
                thought="Generated complete itinerary with all details",
                tool_output={"itinerary": itinerary}
            )
            trace.thoughts.append(final_thought)
            
            # Build final answer
            trace.final_answer = json.dumps(itinerary, indent=2)
            trace.success = True
            trace.total_steps = step
            
        except Exception as e:
            trace.error = str(e)
            trace.success = False
        
        trace.execution_time_ms = (time.time() - start_time) * 1000
        return trace
    
    def _parse_constraints(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse query to extract travel constraints"""
        # Simplified constraint extraction
        # In production, use LLM to parse query
        
        constraints = {
            "duration_days": context.get("duration_days", 3),
            "budget_usd": context.get("budget_usd", 1000),
            "travelers": context.get("travelers", 1),
            "interests": context.get("interests", ["culture", "food"]),
            "location": context.get("destination"),
            "transport_mode": context.get("transport_mode", "walking"),
            "needs_flight": context.get("needs_flight", False),
            "origin": context.get("origin"),
            "destination": context.get("destination"),
            "start_date": context.get("start_date")
        }
        
        return constraints
    
    def _generate_itinerary(
        self,
        pois: List[Dict[str, Any]],
        constraints: Dict[str, Any],
        trace: AgentTrace
    ) -> Dict[str, Any]:
        """Generate final itinerary from gathered data"""
        
        duration_days = constraints.get("duration_days", 3)
        budget = constraints.get("budget_usd", 1000)
        
        # Distribute POIs across days
        pois_per_day = max(1, len(pois) // duration_days)
        
        days = []
        total_cost = 0
        
        for day_num in range(1, duration_days + 1):
            start_idx = (day_num - 1) * pois_per_day
            end_idx = start_idx + pois_per_day
            day_pois = pois[start_idx:end_idx]
            
            activities = []
            for poi in day_pois:
                activity = {
                    "time": f"{8 + len(activities) * 2}:00",
                    "name": poi.get("name"),
                    "type": poi.get("type"),
                    "location": poi.get("address"),
                    "duration_hours": 2,
                    "estimated_cost": poi.get("price_level", 2) * 20,
                    "rating": poi.get("rating")
                }
                activities.append(activity)
                total_cost += activity["estimated_cost"]
            
            days.append({
                "day": day_num,
                "date": f"2026-01-{day_num + 10}",  # Example dates
                "activities": activities,
                "meals": [
                    {"type": "breakfast", "cost": 15},
                    {"type": "lunch", "cost": 25},
                    {"type": "dinner", "cost": 40}
                ],
                "daily_cost": sum(a["estimated_cost"] for a in activities) + 80
            })
        
        return {
            "id": f"itin_{int(time.time())}",
            "title": f"{duration_days}-Day Itinerary",
            "destination": constraints.get("location", "Destination"),
            "duration_days": duration_days,
            "travelers": constraints.get("travelers", 1),
            "days": days,
            "summary": {
                "total_activities": len(pois),
                "total_cost_usd": total_cost + (80 * duration_days),
                "within_budget": total_cost <= budget,
                "transport_modes": ["walking", "transit"],
                "difficulty": "moderate"
            },
            "pois": pois[:10],  # Include POI details
            "reasoning_steps": trace.total_steps,
            "confidence_score": 0.85
        }
