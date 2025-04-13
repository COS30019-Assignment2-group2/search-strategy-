import sys
from collections import deque

def read_problem_file(filename):
    nodes = {}
    edges = {}
    origin = None
    destinations = []
    
    with open(filename, 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            if line.endswith(':'):
                section = line[:-1].lower()
                continue
            
            if section == 'nodes':
                node_id, coords = line.split(':', 1)
                node_id = int(node_id.strip())
                coords = coords.strip()[1:-1].split(',')
                x, y = int(coords[0]), int(coords[1])
                nodes[node_id] = (x, y)
            
            elif section == 'edges':
                edge_desc, cost = line.split(':', 1)
                edge_desc = edge_desc.strip()[1:-1].split(',')
                from_node, to_node = int(edge_desc[0]), int(edge_desc[1])
                cost = int(cost.strip())
                
                if from_node not in edges:
                    edges[from_node] = {}
                edges[from_node][to_node] = cost
            
            elif section == 'origin':
                origin = int(line.strip())
            
            elif section == 'destinations':
                destinations = [int(dest.strip()) for dest in line.split(';')]
    
    return nodes, edges, origin, destinations

def breadth_first_search(nodes, edges, origin, destinations):
    frontier = deque([(origin, [origin])])
    explored = set()
    nodes_created = 1 
    
    while frontier:
        current, path = frontier.popleft()

        if current in destinations:
            return path, current, nodes_created

        if current in explored:
            continue

        explored.add(current)

        neighbors = edges.get(current, {})
        sorted_neighbors = sorted(neighbors.keys())
        
        for neighbor in sorted_neighbors:
            if neighbor not in explored:
                new_path = path + [neighbor]
                frontier.append((neighbor, new_path))
                nodes_created += 1

    return None, None, nodes_created

def main():
    print("Starting program...")
    print(f"Arguments: {sys.argv}")
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        return
    
    filename = sys.argv[1]
    method = sys.argv[2].upper()
    
    nodes, edges, origin, destinations = read_problem_file(filename)
    
    if method == "BFS":
        path, goal, nodes_created = breadth_first_search(nodes, edges, origin, destinations)
        
        if path:
            print(f"{filename} {method}")
            print(f"{goal} {nodes_created}")
            print(" ".join(str(node) for node in path))
        else:
            print(f"{filename} {method}")
            print("No solution found")
    else:
        print(f"Method {method} not implemented")

if __name__ == "__main__":
    main()