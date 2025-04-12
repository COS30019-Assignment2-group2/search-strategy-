import sys
import time

def parse_input_file(filename):
    """
    Parses the input file containing graph information.

    Args:
        filename (str): The path to the input file.

    Returns:
        tuple: A tuple containing:
            - graph (dict): Adjacency list representation {node: {neighbor: cost}}.
            - origin (int): The starting node.
            - destinations (set): A set of destination nodes.
            - node_coords (dict): A dictionary mapping node IDs to their (x, y) coordinates (not used by DFS directly, but part of the spec).
    """
    nodes = {}
    edges = {}
    origin = None
    destinations = set()
    mode = None # Can be 'Nodes', 'Edges', 'Origin', 'Destinations'

    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): # Skip empty lines and comments
                    continue

                if line == "Nodes:":
                    mode = 'Nodes'
                    continue
                elif line == "Edges:":
                    mode = 'Edges'
                    # Initialize graph structure based on collected nodes
                    graph = {node_id: {} for node_id in nodes}
                    continue
                elif line == "Origin:":
                    mode = 'Origin'
                    continue
                elif line == "Destinations:":
                    mode = 'Destinations'
                    continue

                if mode == 'Nodes':
                    # Example: 1: (4,1)
                    parts = line.split(':')
                    node_id = int(parts[0].strip())
                    coords_str = parts[1].strip().strip('()')
                    x, y = map(int, coords_str.split(','))
                    nodes[node_id] = (x, y)
                elif mode == 'Edges':
                    # Example: (2,1): 4
                    parts = line.split(':')
                    edge_str = parts[0].strip().strip('()')
                    from_node, to_node = map(int, edge_str.split(','))
                    cost = int(parts[1].strip())
                    if from_node in graph:
                         # Store neighbors with their costs
                        graph[from_node][to_node] = cost
                    else:
                        print(f"Warning: Edge specified for non-existent node {from_node}. Ignoring edge {line}", file=sys.stderr)

                elif mode == 'Origin':
                    origin = int(line)
                elif mode == 'Destinations':
                    dest_nodes = line.split(';')
                    for dest in dest_nodes:
                        dest = dest.strip()
                        if dest:
                            destinations.add(int(dest))

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing file '{filename}': {e}", file=sys.stderr)
        sys.exit(1)

    if origin is None or not destinations:
        print(f"Error: Origin or Destinations not specified correctly in '{filename}'.", file=sys.stderr)
        sys.exit(1)

    return graph, origin, destinations, nodes

def depth_first_search(graph, origin, destinations):
    """
    Performs Depth-First Search to find a path from origin to any destination.

    Args:
        graph (dict): Adjacency list representation {node: {neighbor: cost}}.
        origin (int): The starting node.
        destinations (set): A set of destination nodes.

    Returns:
        tuple: A tuple containing:
            - path (list | None): The path found as a list of nodes, or None if no path exists.
            - nodes_expanded (int): The number of nodes expanded during the search.
    """
    if origin in destinations:
        return [origin], 0 # Path is just the origin, 0 expansions

    stack = [(origin, [origin])]  # Stack stores tuples of (current_node, path_to_current_node)
    visited = {origin}         # Set to keep track of visited nodes to avoid cycles
    nodes_expanded = 0

    while stack:
        (current_node, path) = stack.pop()
        nodes_expanded += 1 # Count node expansions (when taken off the stack for processing)

        # Get neighbors and sort them by node ID in ascending order [cite: 24]
        neighbors = sorted(graph.get(current_node, {}).keys())

        # Note: The assignment asks to prioritize neighbors by ascending order.
        # For DFS stack (LIFO), we add neighbors in reverse sorted order so that
        # the smallest node ID gets popped and explored first.
        for neighbor in reversed(neighbors):
            if neighbor in destinations:
                # Goal found
                return path + [neighbor], nodes_expanded
            
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return None, nodes_expanded # No path found

# --- Main execution logic ---
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        print("Example: python search.py problem1.txt DFS")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper() # Ensure method is uppercase for comparison

    if method != "DFS":
        print(f"Error: Method '{method}' is not implemented or supported by this script.", file=sys.stderr)
        print("This script currently only supports 'DFS'.")
        sys.exit(1)

    # Parse the input file
    graph, origin, destinations, _ = parse_input_file(filename) # node_coords not needed for DFS pathfinding logic

    # Perform the search
    start_time = time.time()
    path, nodes_expanded = depth_first_search(graph, origin, destinations)
    end_time = time.time()

    # Print output in the specified format [cite: 33]
    print(f"{filename} {method}") # First line: filename and method
    if path:
        goal_node = path[-1]
        path_str = " ".join(map(str, path)) # Format path as space-separated string
        print(f"{goal_node} {nodes_expanded}") # Second line: goal node and number of nodes expanded
        print(path_str) # Third line: the path
    else:
        # If no path is found, the assignment doesn't explicitly state the output format.
        # Printing a message indicating failure seems reasonable.
        print("No path found.")
        print(f"Nodes expanded: {nodes_expanded}")


    # Optional: Print execution time
    # print(f"\nExecution time: {end_time - start_time:.4f} seconds", file=sys.stderr)