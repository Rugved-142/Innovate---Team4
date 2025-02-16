import folium
from typing import List, Dict

def create_map(routes: List[Dict], output_file: str):
    """Create a folium map visualization of the routes"""
    # Center map on Boston
    m = folium.Map(location=[42.3601, -71.0589], zoom_start=12)
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'darkgreen']
    
    for i, route in enumerate(routes):
        color = colors[i % len(colors)]
        
        # Create route line
        coordinates = []
        for stop in route['stops']:
            coordinates.append([stop['latitude'], stop['longitude']])
            
            # Add marker for each stop
            folium.CircleMarker(
                location=[stop['latitude'], stop['longitude']],
                radius=8,
                color=color,
                fill=True,
                popup=f"Request ID: {stop['request_id']}<br>Type: {stop['waste_type']}"
            ).add_to(m)
        
        # Draw route line only if coordinates exist
        if coordinates:
            folium.PolyLine(
                coordinates,
                weight=2,
                color=color,
                opacity=0.8
            ).add_to(m)
    
    m.save(output_file)
