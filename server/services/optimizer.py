from typing import List
from ..models.request import WasteRequest
from ..models.vehicle import Vehicle
from ..utils.geocalc import calculate_distance
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class RouteOptimizer:
    def __init__(self):
        self.solver = None
        
    def optimize(self, vehicles: List[Vehicle], requests: List[WasteRequest]):
        """
        Optimize routes using Google OR-Tools
        """
        # Create distance matrix
        locations = [(v.current_latitude, v.current_longitude) for v in vehicles]
        locations.extend([(r.latitude, r.longitude) for r in requests])
        
        distance_matrix = []
        for i in range(len(locations)):
            row = []
            for j in range(len(locations)):
                if i == j:
                    row.append(0)
                else:
                    dist = calculate_distance(
                        locations[i][0], locations[i][1],
                        locations[j][0], locations[j][1]
                    )
                    row.append(int(dist * 1000))  # Convert to meters
            distance_matrix.append(row)
            
        # Create routing model
        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix),
            len(vehicles),
            0  # depot
        )
        
        routing = pywrapcp.RoutingModel(manager)
        
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]
            
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        # Add capacity constraints
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            if from_node < len(vehicles):
                return 0
            return int(requests[from_node - len(vehicles)].estimated_volume * 100)
            
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        
        for vehicle in vehicles:
            routing.AddDimensionWithVehicleCapacity(
                demand_callback_index,
                0,  # null capacity slack
                [int(v.capacity * 100) for v in vehicles],  # vehicle maximum capacities
                True,  # start cumul to zero
                'Capacity'
            )
            
        # Set first solution strategy
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        
        # Solve
        solution = routing.SolveWithParameters(search_parameters)
        
        if not solution:
            return []
            
        # Extract routes
        routes = []
        for vehicle_id in range(len(vehicles)):
            route = []
            index = routing.Start(vehicle_id)
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                if node_index >= len(vehicles):
                    request = requests[node_index - len(vehicles)]
                    route.append({
                        "request_id": request.id,
                        "latitude": request.latitude,
                        "longitude": request.longitude,
                        "waste_type": request.waste_type
                    })
                index = solution.Value(routing.NextVar(index))
            routes.append({
                "vehicle_id": vehicles[vehicle_id].id,
                "stops": route
            })
            
        return routes