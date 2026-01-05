# TravelAgent Pro - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you run TravelAgent Pro locally and test the agentic AI travel planner.

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional, recommended)

## Option 1: Quick Start (Without Docker)

### 1. Set up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example ../.env

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 2. Test the API

Open http://localhost:8000/docs in your browser to access the interactive API documentation (Swagger UI).

#### Example: Create a Travel Plan

**Using Swagger UI:**
1. Go to http://localhost:8000/docs
2. Expand `POST /api/v1/plans`
3. Click "Try it out"
4. Use this example request:

```json
{
  "query": "Plan a 3-day trip to Tokyo for 2 people, budget $2000, interested in culture and food",
  "constraints": {
    "duration_days": 3,
    "budget_usd": 2000,
    "travelers": 2,
    "interests": ["culture", "food"],
    "destination": "Tokyo"
  }
}
```

5. Click "Execute"

**Using cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/plans" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Plan a 3-day trip to Tokyo",
    "constraints": {
      "duration_days": 3,
      "budget_usd": 2000,
      "travelers": 2,
      "interests": ["culture", "food"],
      "destination": "Tokyo"
    }
  }'
```

**Expected Response:**

```json
{
  "plan_id": "itin_1704389123",
  "status": "completed",
  "itinerary": {
    "id": "itin_1704389123",
    "title": "3-Day Itinerary",
    "destination": "Tokyo",
    "duration_days": 3,
    "travelers": 2,
    "days": [
      {
        "day": 1,
        "date": "2026-01-11",
        "activities": [
          {
            "time": "8:00",
            "name": "Sample culture Place 1",
            "type": "attraction",
            "location": "Sample Address 1",
            "duration_hours": 2,
            "estimated_cost": 40,
            "rating": 4.5
          }
        ],
        "meals": [
          {"type": "breakfast", "cost": 15},
          {"type": "lunch", "cost": 25},
          {"type": "dinner", "cost": 40}
        ],
        "daily_cost": 120
      }
    ],
    "summary": {
      "total_activities": 2,
      "total_cost_usd": 320,
      "within_budget": true,
      "transport_modes": ["walking", "transit"],
      "difficulty": "moderate"
    },
    "pois": [...],
    "reasoning_steps": 3,
    "confidence_score": 0.85
  },
  "reasoning_trace": [
    {
      "step": 1,
      "thought": "I need to find places of interest for: ['culture', 'food']",
      "tool_name": "map_search_places",
      "tool_input": {"query": "...", "location": "Tokyo"},
      "tool_output": {"success": true, "data": [...]}
    },
    {
      "step": 2,
      "thought": "Computing optimal route between points of interest",
      "tool_name": "map_compute_routes",
      "tool_output": {...}
    },
    {
      "step": 3,
      "thought": "Generated complete itinerary with all details",
      "tool_output": {"itinerary": {...}}
    }
  ],
  "confidence_score": 0.85,
  "execution_time_ms": 342.5
}
```

## Option 2: Docker Compose (Full Stack)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## Understanding the Response

### Key Components:

1. **Itinerary**: Complete day-by-day travel plan
   - Activities with timing and costs
   - Meals recommendations
   - Daily budgets

2. **Reasoning Trace**: See how the AI agent thinks
   - Step-by-step thought process
   - Tool calls and their results
   - Verification steps

3. **Metadata**:
   - `confidence_score`: AI's confidence in the plan (0-1)
   - `execution_time_ms`: How long it took to generate
   - `reasoning_steps`: Number of reasoning iterations

## Available Tools

The agent uses these tools to plan your trip:

```bash
# List all available tools
curl http://localhost:8000/api/v1/tools
```

**Tools:**
- `map_search_places`: Find POIs matching criteria
- `map_compute_routes`: Calculate routes between locations
- `map_search_along_route`: Find places along a route
- `map_search_central_places`: Find meeting points
- `travel_search_flights`: Search for flights
- `travel_search_trains`: Search for trains

## Example Queries

### Simple City Trip
```json
{
  "query": "Weekend trip to Paris",
  "constraints": {
    "duration_days": 2,
    "destination": "Paris"
  }
}
```

### Complex Multi-Constraint Trip
```json
{
  "query": "5-day family trip to Barcelona with kids",
  "constraints": {
    "duration_days": 5,
    "budget_usd": 3000,
    "travelers": 4,
    "interests": ["family", "beach", "culture"],
    "destination": "Barcelona",
    "transport_mode": "transit"
  }
}
```

### With Flight Search
```json
{
  "query": "Business trip from SF to NY",
  "constraints": {
    "duration_days": 2,
    "origin": "SFO",
    "destination": "JFK",
    "needs_flight": true,
    "start_date": "2026-02-15"
  }
}
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check |
| `/api/v1/plans` | POST | Create travel plan |
| `/api/v1/plans/{id}` | GET | Get existing plan |
| `/api/v1/tools` | GET | List available tools |
| `/docs` | GET | Interactive API docs |

## Monitoring Agent Reasoning

The `reasoning_trace` in the response shows you exactly how the AI agent:
1. Understood your query
2. Decided which tools to use
3. Executed tools and processed results
4. Verified information
5. Generated the final itinerary

This transparency is key to trustworthy AI - you can see and audit every decision.

## Next Steps

1. **Explore API Docs**: http://localhost:8000/docs
2. **Read Architecture**: See `ARCHITECTURE.md`
3. **Business Strategy**: See `BUSINESS_STRATEGY.md`
4. **Customize**: Modify tools in `backend/app/tools/`
5. **Add Real APIs**: Replace mock data with real API integrations

## Troubleshooting

### Port Already in Use
```bash
# Use different port
uvicorn app.main:app --port 8001
```

### Import Errors
```bash
# Make sure you're in the backend directory
cd backend
# And virtual environment is activated
source venv/bin/activate
```

### Dependencies Issues
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Project Structure

```
travelagent-pro/
├── backend/
│   ├── app/
│   │   ├── agents/         # AI agents (TravelPlannerAgent)
│   │   ├── tools/          # Tools (maps, flights, etc.)
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── schemas/        # Pydantic models
│   │   └── main.py         # FastAPI app
│   └── requirements.txt
├── README.md
├── ARCHITECTURE.md          # Technical details
├── BUSINESS_STRATEGY.md     # Business plan
├── QUICKSTART.md           # This file
├── .env.example
└── docker-compose.yml
```

## Support

- **Documentation**: See README.md
- **API Docs**: http://localhost:8000/docs
- **Issues**: Open GitHub issue
- **Email**: support@travelagent.pro

## What's Next?

This is a working MVP with:
- ✅ Agentic AI system (STAgent-inspired)
- ✅ 6 specialized tools
- ✅ ReAct-style reasoning
- ✅ Self-verification
- ✅ Explainable outputs
- ✅ Enterprise architecture

**To Make it Production-Ready:**
1. Replace mock data with real API integrations
2. Add authentication (JWT)
3. Implement database persistence
4. Add caching (Redis)
5. Set up monitoring and logging
6. Deploy to cloud (AWS/GCP/Azure)
7. Build frontend UI

---

**Happy Planning!** 🌍✈️
