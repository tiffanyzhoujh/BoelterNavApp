import json, csv, math, networkx as nx, os
from itertools import combinations

def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def load_coordinates(csv_files):
    coordinates = {}
    for csv_file in csv_files:
        with open(os.path.join('data', csv_file), newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                label, x, y = row
                coordinates[label] = (int(x), int(y))
    return coordinates

def load_edges(json_files):
    adjacency_list = {}
    for json_file in json_files:
        with open(os.path.join('data', json_file)) as file:
            edges = json.load(file)
            for node, neighbors in edges.items():
                if node not in adjacency_list:
                    adjacency_list[node] = set()
                adjacency_list[node].update(map(str, neighbors))
    return adjacency_list

def build_weighted_graph(coords, adjacency_list, elevator_connections):
    G = nx.Graph()
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            if node in coords and neighbor in coords:
                weight = euclidean_distance(coords[node], coords[neighbor])
                G.add_edge(node, neighbor, weight=weight)
    for elevator in elevator_connections:
        for floor_a, floor_b in combinations(elevator, 2):
            if floor_a in coords and floor_b in coords:
                G.add_edge(floor_a, floor_b, weight=0.1)
    return G

coord_files = [f"{f}f-coord.csv" for f in range(1, 10)]
edge_files = [f"{f}f-edges.json" for f in range(1, 10)]

elevator_connections = [
    ["1f-11","2f-5","3f-15","4f-71","5f-42","6f-57","7f-60","8f-25"],
    ["1f-22","2f-17","3f-23","4f-39","5f-58","6f-35","7f-38","8f-22"],
    ["2f-36","3f-59","4f-5","5f-36","6f-2","7f-2","8f-3","9f-3"],
    ["2f-50","3f-37","4f-27","5f-22","6f-21","7f-17","8f-15","9f-17"]
]

_coordinates = load_coordinates(coord_files)
_edges = load_edges(edge_files)
_graph = build_weighted_graph(_coordinates, _edges, elevator_connections)

def get_shortest_path(start, end):
    if start not in _graph.nodes or end not in _graph.nodes:
        raise ValueError("Invalid start or destination node.")

    path = nx.shortest_path(_graph, source=start, target=end, weight="weight")

    result = []
    for node in path:
        if node not in _coordinates:
            continue
        x, y = _coordinates[node]
        floor = node.split('-')[0]
        result.append({
            "name": node,
            "x": x,
            "y": y,
            "floor": floor
        })

    return result

def get_floorplans(path):
    floors_in_order = []
    seen = set()

    for node in path:
        floor = node['floor']
        if floor not in seen:
            floors_in_order.append(floor)
            seen.add(floor)
    print("floors in order:")
    print(floors_in_order)

    floorplan_paths = [
        os.path.join('png_floorplans', f"floor-{floor[0]}-new.png")
        for floor in floors_in_order
    ]

    return floorplan_paths
