import sys #  system-specific functions
import math #  math functions.
import heapq #  heap queue algorithm, efficient data structures for finding element
import re # regular expressions
import time # time-related functions

# --- Data Structures ---

class Node:
    """Represents a node in the graph."""
    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x = x
        self.y = y
        self.neighbors = {} 

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost

    def get_coords(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Node({self.id}, ({self.x},{self.y}))"

class Graph:
    """Represents the graph."""
    def __init__(self):
        self.nodes = {} 
        self.origin_id = None
        self.destination_ids = set()

    def add_node(self, node_id, x, y):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, x, y)

    def add_edge(self, from_node_id, to_node_id, cost):
        if from_node_id in self.nodes:
            self.nodes[from_node_id].add_neighbor(to_node_id, cost)
            
    def set_origin(self, node_id):
        self.origin_id = node_id

    def add_destination(self, node_id):
        self.destination_ids.add(node_id)

    def get_node(self, node_id):
        return self.nodes.get(node_id)

# --- Heuristic Function ---

def euclidean_distance(node1_coords, node2_coords):
    """Calculates the Euclidean distance between two points."""
    x1, y1 = node1_coords
    x2, y2 = node2_coords
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def heuristic(graph, current_node_id):
    """Calculates the heuristic value (h(n)) for A*.
       Uses the minimum Euclidean distance to any destination node.
    """
    current_node = graph.get_node(current_node_id)
    if not current_node or not graph.destination_ids:
        return float('inf') 

    min_dist = float('inf')
    current_coords = current_node.get_coords()

    for dest_id in graph.destination_ids:
        dest_node = graph.get_node(dest_id)
        if dest_node:
            dist = euclidean_distance(current_coords, dest_node.get_coords())
            min_dist = min(min_dist, dist)

    return min_dist

# --- A* Search Algorithm ---

def a_star_search(graph):
    """Performs A* search on the graph."""
    start_node_id = graph.origin_id
    destination_ids = graph.destination_ids

    # Priority Queue (Frontier): Stores tuples (f_cost, node_id, g_cost, path, timestamp)
    entry_count = 0 
    frontier = [(heuristic(graph, start_node_id), start_node_id, 0, [start_node_id], entry_count)]
    entry_count += 1
    # Explored set: Stores {node_id: g_cost} to keep track of the lowest cost found so far to reach a node
    explored = {}
    nodes_created = 1 #

    while frontier:
        f_cost_est, current_node_id, g_cost, path, _ = heapq.heappop(frontier)

        # Goal Check
        if current_node_id in destination_ids:
            return path, nodes_created # Return the path and node count

        # Check if we've found a better path 
        if current_node_id in explored and explored[current_node_id] <= g_cost:
            continue 

        # Add to explored set with its cost
        explored[current_node_id] = g_cost

        # Expand neighbors
        current_node = graph.get_node(current_node_id)
        if not current_node: continue

        for neighbor_id, step_cost in current_node.neighbors.items():
            if graph.get_node(neighbor_id) is None: continue # Ensure neighbor exists

            new_g_cost = g_cost + step_cost

            #check if this new path is better
            if neighbor_id in explored and explored[neighbor_id] <= new_g_cost:
                 continue 
            # Calculate f_cost for the neighbor
            h_cost = heuristic(graph, neighbor_id)
            f_cost = new_g_cost + h_cost
            new_path = path + [neighbor_id]
            nodes_created += 1

            # Add neighbor to the frontier
            heapq.heappush(frontier, (f_cost, neighbor_id, new_g_cost, new_path, entry_count))
            entry_count += 1

    return None, nodes_created # No path found

# --- File Parsing ---

def parse_input_file(filename):
    """Parses the problem definition file."""
    graph = Graph()
    section = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): 
                continue

            if line.lower() == "nodes:":
                section = "nodes"
            elif line.lower() == "edges:":
                section = "edges"
            elif line.lower() == "origin:":
                section = "origin"
            elif line.lower() == "destinations:":
                section = "destinations"
            else:
                if section == "nodes":
                    match = re.match(r'(\d+):\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', line)
                    if match:
                        node_id, x, y = map(int, match.groups())
                        graph.add_node(node_id, x, y)
                elif section == "edges":
                    match = re.match(r'\(\s*(\d+)\s*,\s*(\d+)\s*\):\s*(\d+)', line)
                    if match:
                        from_id, to_id, cost = map(int, match.groups())
                        graph.add_edge(from_id, to_id, cost)
                elif section == "origin":
                    graph.set_origin(int(line))
                elif section == "destinations":
                    dest_ids = map(int, line.split(';'))
                    for dest_id in dest_ids:
                        graph.add_destination(dest_id)

    return graph

# --- Main ---

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search.py <PathFinder-test.txt> <method>")
        print("Example: python search.py PathFinder-test.txt AS")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper() # Convert method to uppercase

    if method != "AS":
        print(f"Error: Method '{method}' is not implemented in this script. Only 'AS' is supported.")
        sys.exit(1)

    try:
        graph = parse_input_file(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing file '{filename}': {e}")
        sys.exit(1)

    # --- Execute A* Search ---
    if method == "AS":
        result_path, nodes_created_count = a_star_search(graph)

        # --- Format Output ---
        if result_path:
            goal_node = result_path[-1]
            path_str = " -> ".join(map(str, result_path))
            print(f"{filename} {method}") 
            print(f"{goal_node} {nodes_created_count}") 
            print(f"{path_str}") 
        else:
            # Handle case where no path is found 
            print(f"{filename} {method}")
            print("No path found.")

    # Add logic for other search methods 
    
    # run cmd python astar_search.py PathFinder-test.txt AS