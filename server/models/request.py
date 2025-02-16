from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WasteRequest(BaseModel):
    id: str
    latitude: float
    longitude: float
    waste_type: str
    priority: int
    request_time: datetime
    estimated_volume: Optional[float]
    address: str