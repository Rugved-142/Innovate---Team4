import click
import requests
from typing import List
import json
from .visualizer import create_map

@click.group()
def cli():
    """Waste Collection Route Optimization CLI"""
    pass

@cli.command()
@click.option('--count', default=10, help='Number of simulated requests to generate')
def simulate(count: int):
    """Generate simulated waste collection requests"""
    response = requests.post(f"http://localhost:8000/simulate/requests?count={count}")
    requests_data = response.json()
    click.echo(f"Generated {len(requests_data)} requests:")
    click.echo(json.dumps(requests_data, indent=2))

@cli.command()
@click.option('--vehicles', type=click.Path(exists=True), help='Path to vehicles JSON file')
@click.option('--requests_path', type=click.Path(exists=True), help='Path to requests JSON file')
def optimize(vehicles: str, requests_path: str):
    """Optimize routes for given vehicles and requests"""
    with open(vehicles) as f:
        vehicles_data = json.load(f)
    with open(requests_path) as f:
        requests_data = json.load(f)
        
    response = requests.post(
        "http://localhost:8000/optimize/routes",
        json={
            "vehicles": vehicles_data,
            "requests": requests_data
        }
    )
    
    routes = response.json()
    click.echo("Optimized routes:")
    click.echo(json.dumps(routes, indent=2))
    
    # Generate visualization
    create_map(routes, "routes.html")
    click.echo("Route visualization saved to routes.html")

if __name__ == '__main__':
    cli()
