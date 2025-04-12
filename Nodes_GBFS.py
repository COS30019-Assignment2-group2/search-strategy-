import heapq


def read_graph(file_path):
    nodes = {}
    edges = {}
    origin = None
    destinations = []

    with open(file_path, 'r') as file:
        content = file.readlines()
        state = None
        for line in content:
            line = line.strip()
            if not line:
                continue
            elif line.startswith('Nodes:'):
                state = 'nodes'
            elif line.startswith('Edges:'):
                state = 'edges'
            elif line.startswith('Origin:'):
                state = 'origin'
            elif line.startswith('Destinations:'):
                state = 'destinations'
            else:
                if state == 'nodes':
                    node_id, coords = line.split(': ')
                    x, y = map(int, coords.strip('()').split(','))
                    nodes[int(node_id)] = (x, y)
                elif state == 'edges':
                    edge, cost = line.split(': ')
                    start, end = map(int, edge.strip('()').split(','))
                    edges[(start, end)] = int(cost)
                elif state == 'origin':
                    origin = int(line)
                elif state == 'destinations':
                    destinations = list(map(int, line.split(';')))

    return nodes, edges, origin, destinations


def dfs(nodes, edges, origin, destination):
    stack = [(origin, [origin])]
    visited = set()

    while stack:
        node, path = stack.pop()
        if node == destination:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in sorted([end for start, end in edges if start == node]):
                stack.append((neighbor, path + [neighbor]))

    return None


def bfs(nodes, edges, origin, destination):
    queue = [(origin, [origin])]
    visited = set()

    while queue:
        node, path = queue.pop(0)
        if node == destination:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in sorted([end for start, end in edges if start == node]):
                queue.append((neighbor, path + [neighbor]))

    return None


def heuristic(a, b, nodes):
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    return abs(x1 - x2) + abs(y1 - y2)


def gbfs(nodes, edges, origin, destination):
    heap = [(heuristic(origin, destination, nodes), origin, [origin])]
    visited = set()

    while heap:
        _, node, path = heapq.heappop(heap)
        if node == destination:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in sorted([end for start, end in edges if start == node]):
                heapq.heappush(heap, (heuristic(neighbor, destination, nodes), neighbor, path + [neighbor]))

    return None


def astar(nodes, edges, origin, destination):
    open_set = [(0 + heuristic(origin, destination, nodes), origin, [origin], 0)]
    closed_set = set()

    while open_set:
        _, node, path, cost = heapq.heappop(open_set)
        if node == destination:
            return path
        if node not in closed_set:
            closed_set.add(node)
            for neighbor in sorted([end for start, end in edges if start == node]):
                new_cost = cost + edges[(node, neighbor)]
                heapq.heappush(open_set, (new_cost + heuristic(neighbor, destination, nodes), neighbor, path + [neighbor], new_cost))

    return None


def custom_uninformed_search(nodes, edges, origin, destination):
    stack = [(origin, [origin])]
    visited = set()
    import random
    while stack:
        node, path = stack.pop()
        if node == destination:
            return path
        if node not in visited:
            visited.add(node)
            neighbors = [end for start, end in edges if start == node]
            random.shuffle(neighbors)
            for neighbor in sorted(neighbors):
                stack.append((neighbor, path + [neighbor]))

    return None


def custom_informed_search(nodes, edges, origin, destination):
    heap = [(heuristic(origin, destination, nodes), origin, [origin], 0)]
    visited = set()
    while heap:
        _, node, path, cost = heapq.heappop(heap)
        if node == destination:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in sorted([end for start, end in edges if start == node]):
                new_cost = cost + edges[(node, neighbor)]
                new_heuristic = heuristic(neighbor, destination, nodes)
                heapq.heappush(heap, (new_heuristic + new_cost * 0.5, neighbor, path + [neighbor], new_cost))

    return None


def main():
    import sys
    if len(sys.argv)!= 3:
        print('Usage: python search.py <filename> <method>')
        return

    file_path = sys.argv[1]
    method = sys.argv[2]

    nodes, edges, origin, destinations = read_graph(file_path)

    for destination in destinations:
        if method == 'DFS':
            path = dfs(nodes, edges, origin, destination)
        elif method == 'BFS':
            path = bfs(nodes, edges, origin, destination)
        elif method == 'GBFS':
            path = gbfs(nodes, edges, origin, destination)
        elif method == 'AS':
            path = astar(nodes, edges, origin, destination)
        elif method == 'CUS1':
            path = custom_uninformed_search(nodes, edges, origin, destination)
        elif method == 'CUS2':
            path = custom_informed_search(nodes, edges, origin, destination)
        else:
            print('Invalid method')
            return

        if path:
            print(f'{file_path} {method} {destination} {len(path)}')
            print(' '.join(map(str, path)))
        else:
            print(f'{file_path} {method} {destination} 0')


if __name__ == "__main__":
    main()
