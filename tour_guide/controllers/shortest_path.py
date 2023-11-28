from fastapi import HTTPException, APIRouter
from tour_guide.validators.shortest_path import shortestPathRequestFormat
import networkx as nx
from math import radians, sin, cos, sqrt, atan2
import pandas as pd


router = APIRouter()

def calculate_shortest_path(coordinates):
    # Create a complete graph with distances based on coordinates
    G = nx.complete_graph(len(coordinates))

    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            distance = calculate_distance(coordinates[i], coordinates[j])
            G[i][j]['weight'] = distance
            G[j][i]['weight'] = distance

    # Find the Hamiltonian path that minimizes the total distance
    hamiltonian_path = nx.approximation.traveling_salesman_problem(G, cycle=False)

    # Ensure the Hamiltonian path starts from the first coordinate
    if hamiltonian_path[0] != 0:
        # Find the index of the first coordinate in the path and rotate the list
        rotate_index = hamiltonian_path.index(0)
        hamiltonian_path = hamiltonian_path[rotate_index:] + hamiltonian_path[:rotate_index]

    # Rearrange coordinates based on the Hamiltonian path
    sorted_coordinates = [coordinates[i] for i in hamiltonian_path]

    return sorted_coordinates


def calculate_distance(coord1, coord2):
    # return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5
    # Haversine formula for distance between two points on a sphere
    R = 6371.0  # Earth radius in kilometers

    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

@router.post("")
async def get_shortest_path(request_body: shortestPathRequestFormat):

    request_data = request_body.dict()

    names = request_data['names']

    df = pd.read_excel('tourist_places.xlsx')

    coordinates = []

    for index, row in df.iterrows():
        coordinates.append([row['Latitude'], row['Longitude'], row['Name']])

    if len(names) < 2:
        raise HTTPException(status_code=400, detail="At least two locations are required.")

    search_coordinates = []
    for coordinate in coordinates:
        if coordinate[2] in names:
            search_coordinates.append([coordinate[0], coordinate[1]])
    
    coordinates = [coord for coord in coordinates if coord[2] in names]
    
    try:
        sorted_coordinates = calculate_shortest_path(search_coordinates)

        response = {}

        places_api_endpoint = "https://www.google.com/maps/search/"

        for coordinate in coordinates:
            params = {
                "api": "1",
                "query": f"restaurants near {coordinate[0]},{coordinate[1]}",
            }
            restaurants_link = places_api_endpoint + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

            params = {
                "api": "1",
                "query": f"hotels near {coordinate[0]},{coordinate[1]}",
            }
            hotels_link = places_api_endpoint + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

            response[coordinate[2]] = {
                'restaurants': restaurants_link,
                'hotels': hotels_link
            }        

        sorted_coordinates = [request_data['current_coordinates']] + sorted_coordinates
        google_maps_url = "https://www.google.com/maps/dir/" + "/".join([f"{lat},{lon}" for lat, lon in sorted_coordinates])

        response['navigation_url'] = google_maps_url
    
        return {"data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("")
async def get_locations():

    location_list = []

    df = pd.read_excel('tourist_places.xlsx')

    for index, row in df.iterrows():
        location_list.append([row['Name'], row['Description']])

    return {'data': location_list}