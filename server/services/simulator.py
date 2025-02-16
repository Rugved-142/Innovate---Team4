import random
from datetime import datetime, timedelta
from ..models.request import WasteRequest
from typing import List
import uuid

class RequestSimulator:
    def __init__(self):
        # Boston geographical boundaries
        self.min_lat = 42.2279
        self.max_lat = 42.3975
        self.min_lon = -71.1912
        self.max_lon = -70.9228
        
        self.waste_types = ["hazardous", "chemical", "medical", "industrial"]
        
    def generate_requests(self, count: int) -> List[WasteRequest]:
        requests = []
        
        for _ in range(count):
            lat = random.uniform(self.min_lat, self.max_lat)
            lon = random.uniform(self.min_lon, self.max_lon)
            
            request = WasteRequest(
                id=str(uuid.uuid4()),
                latitude=lat,
                longitude=lon,
                waste_type=random.choice(self.waste_types),
                priority=random.randint(1, 5),
                request_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                estimated_volume=random.uniform(0.1, 2.0),
                address=f"Sample Address {random.randint(1, 1000)}, Boston, MA"
            )
            
            requests.append(request)
            
        return requests