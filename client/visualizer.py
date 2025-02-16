import folium
from typing import List, Dict
import osmnx as ox
import networkx as nx

def create_map(routes: List[Dict], output_file: str, vehicle_id: str = None):
    """Create a folium map visualization for a specific vehicle or all vehicles."""
    m = folium.Map(location=[42.3601, -71.0589], zoom_start=14)

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'darkgreen']
    graph = ox.graph_from_place("Boston, Massachusetts, USA", network_type="drive")

    # Filter routes if a specific vehicle_id is provided
    if vehicle_id:
        routes = [route for route in routes if route['vehicle_id'] == vehicle_id]

    for i, route in enumerate(routes):
        color = colors[i % len(colors)]

        coordinates = []
        for stop in route['stops']:
            folium.Marker(
                location=[stop['latitude'], stop['longitude']],
                popup=f"Request ID: {stop['request_id']}<br>Type: {stop['waste_type']}",
                icon=folium.Icon(color=color),
            ).add_to(m)

            coordinates.append((stop['latitude'], stop['longitude']))

        # Calculate path using OSMNX
        if len(coordinates) >= 2:
            for j in range(len(coordinates) - 1):
                orig_node = ox.distance.nearest_nodes(graph, coordinates[j][1], coordinates[j][0])
                dest_node = ox.distance.nearest_nodes(graph, coordinates[j + 1][1], coordinates[j + 1][0])

                try:
                    route_nodes = nx.shortest_path(graph, orig_node, dest_node, weight='length')
                    path_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route_nodes]

                    folium.PolyLine(path_coords, color=color, weight=4, opacity=0.7).add_to(m)
                except nx.NetworkXNoPath:
                    print(f"No valid path between stops {coordinates[j]} and {coordinates[j+1]}")

    m.save(output_file)
    print(f"Route visualization saved to {output_file}")
