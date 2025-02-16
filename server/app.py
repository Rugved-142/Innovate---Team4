from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from server.services.optimizer import RouteOptimizer
from .services.simulator import RequestSimulator
from .models.request import WasteRequest
from .models.vehicle import Vehicle

app = FastAPI(title="Waste Collection Optimizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

optimizer = RouteOptimizer()
simulator = RequestSimulator()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/simulate/requests")
async def generate_requests(count: int = 10):
    """Generate simulated waste collection requests"""
    return simulator.generate_requests(count)

@app.post("/optimize/routes")
async def optimize_routes(vehicles: List[Vehicle], requests: List[WasteRequest]):
    """Optimize routes for available vehicles"""
    try:
        routes = optimizer.optimize(vehicles, requests)
        return routes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)