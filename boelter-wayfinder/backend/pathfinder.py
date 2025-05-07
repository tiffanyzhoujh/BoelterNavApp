import json, csv, math, networkx as nx, os
from itertools import combinations
import csv
from PIL import Image, ImageDraw, ImageFont

def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def load_coordinates(csv_files):
    # print("loading coordinates...")
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
    # print("loading edges...")
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


# load the PNG icons 
start_icon_path = os.path.join('assets', 'start.png')
end_icon_path = os.path.join('assets', 'end.png')
start_icon = Image.open(start_icon_path).convert('RGBA')
end_icon = Image.open(end_icon_path).convert('RGBA')
icon_size = (100, 50)
start_icon = start_icon.resize(icon_size, Image.Resampling.LANCZOS)
end_icon = end_icon.resize(icon_size, Image.Resampling.LANCZOS)
# opacity 80%
start_icon_transparent = start_icon.copy()
end_icon_transparent = end_icon.copy()
start_icon_transparent.putalpha(230)
end_icon_transparent.putalpha(230)



def get_shortest_path(start, end):
    # print("looking for shortest path...")
    if start not in _graph.nodes or end not in _graph.nodes:
        # print(start)
        # print(end)
        # print("invalid start or dest node...")
        raise ValueError("Invalid start or destination node.")

    path = nx.shortest_path(_graph, source=start, target=end, weight="weight")
    # print("path found...")
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
    # print("shortest path result:")
    # print(result)
    return result

def get_floorplans(path, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # make sure the folder exists

    floors_in_order = []
    seen = set()

    for node in path:
        floor = node['floor']
        if floor not in seen:
            floors_in_order.append(floor)
            seen.add(floor)

    print("floors in order:")
    print(floors_in_order)

    floor_to_nodes = {}
    for node in path:
        floor = node['floor']
        if floor not in floor_to_nodes:
            floor_to_nodes[floor] = []
        floor_to_nodes[floor].append(node)

    output_paths = []

    for floor in floors_in_order:
        input_png_path = os.path.join('png_floorplans', f"f{floor[0]}.png")
        img = Image.open(input_png_path)
        draw = ImageDraw.Draw(img)
        nodes = floor_to_nodes.get(floor, [])
        # draw the line
        if len(nodes) >= 2:
            for i in range(len(nodes) - 1):
                x1, y1 = nodes[i]['x'], nodes[i]['y']
                x2, y2 = nodes[i + 1]['x'], nodes[i + 1]['y']
                draw.line((x1, y1, x2, y2), fill='#48AEE2', width=20)
        # draw other points
        radius = 8
        for node in nodes:
            x, y = node['x'], node['y']
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='#48AEE2')   
        # draw start and end icons
        start_x, start_y = nodes[0]['x'], nodes[0]['y']
        end_x, end_y = nodes[-1]['x'], nodes[-1]['y']
        img.paste(start_icon_transparent, (start_x - 20, start_y - 20), start_icon_transparent)
        img.paste(end_icon_transparent, (end_x + 20, end_y + 20), end_icon_transparent)

        output_path = os.path.join(output_dir, f"{floor}-path.png")
        img.save(output_path)
        output_paths.append(output_path)

    return output_paths

def draw_arrow(draw, x1, y1, x2, y2, color='light blue', width=30, head_size=48):
    draw.line((x1, y1, x2, y2), fill=color, width=width)

    # Calculate direction vector
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return  # avoid division by zero

    # Normalize direction
    udx = dx / length
    udy = dy / length

    # Arrowhead base position (a bit before the end)
    base_x = x2 - udx * head_size
    base_y = y2 - udy * head_size

    # Perpendicular vectors for arrowhead wings
    perp_x = -udy * head_size / 2
    perp_y = udx * head_size / 2

    # Triangle points
    p1 = (x2, y2)
    p2 = (base_x + perp_x, base_y + perp_y)
    p3 = (base_x - perp_x, base_y - perp_y)

    draw.polygon([p1, p2, p3], fill=color)