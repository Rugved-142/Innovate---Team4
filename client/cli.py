import click
import json
import requests
from .visualizer import create_map

@click.group()
def cli():
    pass

@cli.command()
@click.option('--vehicles', required=True, help='Path to vehicles.json')
@click.option('--requests_path', required=True, help='Path to requests.json')
@click.option('--vehicle-id', required=False, help='Vehicle ID to filter routes')
def optimize(vehicles, requests_path, vehicle_id):
    """Optimize routes."""
    response = requests.post("http://localhost:8000/optimize/routes", json={
        "vehicles": json.load(open(vehicles)),
        "requests": json.load(open(requests_path))
    })

    routes = response.json()
    if vehicle_id:
        filtered_routes = [route for route in routes if route.get('vehicle_id') == vehicle_id]
        print(f"Routes for vehicle '{vehicle_id}': {json.dumps(filtered_routes, indent=2)}")
        create_map(filtered_routes, f"routes_{vehicle_id}.html")
    else:
        print(f"All routes: {json.dumps(routes, indent=2)}")
        create_map(routes, "routes.html")

if __name__ == "__main__":
    cli()
