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
    # only connect the next floor
    for elevator in elevator_connections:
        for i in range(len(elevator) - 1):
            floor_a = elevator[i]
            floor_b = elevator[i + 1]
            if floor_a in coords and floor_b in coords:
                G.add_edge(floor_a, floor_b, weight=100)
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

restrooms_women = {"1": ["1f-8"],
                    "2": ["2f-19"] ,
                    "3": ["3f-13","3f-41"],
                    "4": ["4f-159","4f-74"],
                    "5": ["5f-6","5f-24"],
                    "6": ["6f-18"],
                    "7": ["7f-14","7f-59"],
                    "9": ["9f-5"] }
restrooms_men = {  "1": ["1f-20"],
                    "2": ["2f-3"] ,
                    "3": ["3f-26","3f-55"],
                    "4": ["4f-9","4f-36"],
                    "5": ["5f-63"],
                    "6": ["6f-6", "6f-54"],
                    "7": ["7f-5","7f-35"],
                    "9": ["9f-12"] }
restrooms_allgen = {"5": ["5f-34"],
                    "6": ["6f-33"],
                    "8": ["8f-24"] }

# load the PNG icons 
start_icon_path = os.path.join('assets', 'start_flip.png')
end_icon_path = os.path.join('assets', 'end_new.png')
start_icon = Image.open(start_icon_path).convert('RGBA')
end_icon = Image.open(end_icon_path).convert('RGBA')
icon_size = (200, 200)
start_icon = start_icon.resize(icon_size, Image.Resampling.LANCZOS)
end_icon = end_icon.resize(icon_size, Image.Resampling.LANCZOS)
# opacity 80%
start_icon_transparent = start_icon.copy()
end_icon_transparent = end_icon.copy()

def find_path(start, end):
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

def find_nearest_restroom(start, candidates):
    # return the nearest destination in the list of candidates
    nearest = None
    min_distance = float('inf')

    for candidate in candidates:
        if candidate not in _graph.nodes:
            continue
        try:
            path_length = nx.shortest_path_length(_graph, source=start, target=candidate, weight='weight')
            if path_length < min_distance:
                min_distance = path_length
                nearest = candidate
        except nx.NetworkXNoPath:
            continue

    if nearest is None:
        raise ValueError("No reachable restroom found from start.")
    return nearest

def get_shortest_path(start, end):
    if (start not in _graph.nodes or end not in _graph.nodes) and (end not in ["Nearest Restroom (W)", "Nearest Restroom (M)", "Nearest Restroom (Gender Inclusive)"]):
        raise ValueError("Invalid start or destination node.")

    # special case: nearest restroom search
    start_floor = start[0]
    if (end == "Nearest Restroom (W)"):
        # if start is on floor 1, 2, 6, 9, just one solution
        # if start is on floor 3, 4, 5, 7, two solutions
        # if start is on floor 8, look for solution in 7 and 9
        if start_floor in ["1", "2", "6", "9"]:
            end = restrooms_women[start_floor][0]
        elif start_floor in ["3", "4", "5", "7"]: 
            candidates = restrooms_women[start_floor]
            end = find_nearest_restroom(start, candidates)
        else: 
            candidates = restrooms_women["7"] + restrooms_women["9"]
            end = find_nearest_restroom(start, candidates)
    elif (end == "Nearest Restroom (M)"):
        # if start is on floor 1, 2, 5, 9, just one solution
        # if start is on floor 3, 4, 6, 7, two solutions
        # if start is on floor 8, look for solution in 7 and 9
        if start_floor in ["1", "2", "5", "9"]:
            end = restrooms_men[start_floor][0]
        elif start_floor in ["3", "4", "6", "7"]: 
            candidates = restrooms_men[start_floor]
            end = find_nearest_restroom(start, candidates)
        else: 
            candidates = restrooms_men["7"] + restrooms_men["9"]
            end = find_nearest_restroom(start, candidates)
    elif (end == "Nearest Restroom (Gender Inclusive)"): # on floor 5, 6, 8
        if start_floor in ["1","2","3","4","5"]:
            end = restrooms_allgen["5"][0]
        elif start_floor in ["6"]:
            end = restrooms_allgen["6"][0]
        elif start_floor in ["8","9"]:
            end = restrooms_allgen["8"][0]
        else: # floor 7
            candidates = restrooms_allgen["6"]+restrooms_allgen["8"]
            end = find_nearest_restroom(start, candidates)

    # normal shortest path search
    return find_path(start, end)

def get_floorplans(path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # separate the path into segments based on floor changes
    segments = []
    current_segment = []
    current_floor = None

    for node in path:
        floor = node['floor']
        if current_floor is None:
            current_floor = floor

        if floor == current_floor:
            current_segment.append(node)
        else:
            segments.append((current_floor, current_segment))
            current_segment = [node]
            current_floor = floor

    # add the last segment
    if current_segment:
        segments.append((current_floor, current_segment))

    output_paths = []

    # draw each segment independently
    for idx, (floor, nodes) in enumerate(segments):
        if len(nodes) == 1 and floor != path[-1]['floor']:
            continue

        input_png_path = os.path.join('png_floorplans', f"f{floor[0]}.png")
        img = Image.open(input_png_path)
        draw = ImageDraw.Draw(img)

        # draw the lines
        if len(nodes) >= 2:
            for i in range(len(nodes) - 1):
                x1, y1 = nodes[i]['x'], nodes[i]['y']
                x2, y2 = nodes[i + 1]['x'], nodes[i + 1]['y']
                draw.line((x1, y1, x2, y2), fill='#48AEE2', width=20)

        # other points
        radius = 8
        for node in nodes:
            x, y = node['x'], node['y']
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='#48AEE2')   

        # start and end
        if len(nodes) > 0:
            start_x, start_y = nodes[0]['x'], nodes[0]['y']
            end_x, end_y = nodes[-1]['x'], nodes[-1]['y']
            img.paste(start_icon_transparent, (start_x-180, start_y - 180), start_icon_transparent)
            img.paste(end_icon_transparent, (end_x, end_y - 180), end_icon_transparent)

        # differentiate multiple visits to the same floor
        output_path = os.path.join(output_dir, f"{floor}-{idx}-path.png")
        img.save(output_path)
        output_paths.append(output_path)

    return output_paths
