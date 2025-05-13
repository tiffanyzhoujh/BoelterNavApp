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
    # for elevator in elevator_connections:
    #     for floor_a, floor_b in combinations(elevator, 2):
    #         if floor_a in coords and floor_b in coords:
    #             G.add_edge(floor_a, floor_b, weight=0.1)
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
    if start not in _graph.nodes or end not in _graph.nodes:
        raise ValueError("Invalid start or destination node.")

    path = nx.shortest_path(_graph, source=start, target=end, weight="weight")
    result = []
    print("shortest path result:")
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
        print(node)
    return result

# def get_floorplans(path, output_dir):
#     os.makedirs(output_dir, exist_ok=True)
#     floors_in_order = []
#     seen = set()
#     for node in path:
#         floor = node['floor']
#         if floor not in seen:
#             floors_in_order.append(floor)
#             seen.add(floor)

#     print("floors in order:")
#     print(floors_in_order)

#     floor_to_nodes = {}
#     for node in path:
#         floor = node['floor']
#         if floor not in floor_to_nodes:
#             floor_to_nodes[floor] = []
#         floor_to_nodes[floor].append(node)

#     output_paths = []

#     # get the last floor in the path
#     last_floor = path[-1]['floor']

#     for floor in floors_in_order:
#         nodes = floor_to_nodes.get(floor, [])
        
#         # skip drawing if there's only one point on this floor and it's not the last floor
#         if len(nodes) == 1 and floor != last_floor:
#             continue

#         input_png_path = os.path.join('png_floorplans', f"f{floor[0]}.png")
#         img = Image.open(input_png_path)
#         draw = ImageDraw.Draw(img)

#         # draw the lines
#         if len(nodes) >= 2:
#             for i in range(len(nodes) - 1):
#                 x1, y1 = nodes[i]['x'], nodes[i]['y']
#                 x2, y2 = nodes[i + 1]['x'], nodes[i + 1]['y']
#                 draw.line((x1, y1, x2, y2), fill='#48AEE2', width=20)

#         # draw other points
#         radius = 8
#         for node in nodes:
#             x, y = node['x'], node['y']
#             draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='#48AEE2')   

#         # draw start and end
#         if len(nodes) > 0:
#             start_x, start_y = nodes[0]['x'], nodes[0]['y']
#             end_x, end_y = nodes[-1]['x'], nodes[-1]['y']
#             img.paste(start_icon_transparent, (start_x - 20, start_y - 20), start_icon_transparent)
#             img.paste(end_icon_transparent, (end_x + 20, end_y + 20), end_icon_transparent)

#         output_path = os.path.join(output_dir, f"{floor}-path.png")
#         img.save(output_path)
#         output_paths.append(output_path)

#     return output_paths


import os
from PIL import Image, ImageDraw

def get_floorplans(path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Separate the path into segments based on floor changes
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

    # Add the last segment
    if current_segment:
        segments.append((current_floor, current_segment))

    output_paths = []

    # Draw each segment independently
    for idx, (floor, nodes) in enumerate(segments):
        if len(nodes) == 1 and floor != path[-1]['floor']:
            continue

        input_png_path = os.path.join('png_floorplans', f"f{floor[0]}.png")
        img = Image.open(input_png_path)
        draw = ImageDraw.Draw(img)

        # Draw the lines
        if len(nodes) >= 2:
            for i in range(len(nodes) - 1):
                x1, y1 = nodes[i]['x'], nodes[i]['y']
                x2, y2 = nodes[i + 1]['x'], nodes[i + 1]['y']
                draw.line((x1, y1, x2, y2), fill='#48AEE2', width=20)

        # Draw other points
        radius = 8
        for node in nodes:
            x, y = node['x'], node['y']
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='#48AEE2')   

        # Draw start and end
        if len(nodes) > 0:
            start_x, start_y = nodes[0]['x'], nodes[0]['y']
            end_x, end_y = nodes[-1]['x'], nodes[-1]['y']
            img.paste(start_icon_transparent, (start_x - 20, start_y - 20), start_icon_transparent)
            img.paste(end_icon_transparent, (end_x + 20, end_y + 20), end_icon_transparent)

        # Use the index to differentiate multiple visits to the same floor
        output_path = os.path.join(output_dir, f"{floor}-{idx}-path.png")
        img.save(output_path)
        output_paths.append(output_path)

    return output_paths
