from pydantic import BaseModel
from typing import List, Optional

class Vehicle(BaseModel):
    id: str
    capacity: float
    current_latitude: float
    current_longitude: float
    waste_types: List[str]
    current_load: Optional[float] = 0