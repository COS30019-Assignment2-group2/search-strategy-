import heapq
from collections import deque

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}

goal = 'D'

def dfs(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for neighbor, _ in graph[vertex]:
            if neighbor not in path:
                if neighbor == goal:
                    return path + [neighbor]
                else:
                    stack.append((neighbor, path + [neighbor]))
    return None

def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    while queue:
        (vertex, path) = queue.popleft()
        for neighbor, _ in graph[vertex]:
            if neighbor not in path:
                if neighbor == goal:
                    return path + [neighbor]
                else:
                    queue.append((neighbor, path + [neighbor]))
    return None

def heuristic(node, goal):
    return 1

def gbfs(graph, start, goal):
    priority_queue = [(heuristic(start, goal), start, [start])]
    while priority_queue:
        _, vertex, path = heapq.heappop(priority_queue)
        for neighbor, _ in graph[vertex]:
            if neighbor not in path:
                if neighbor == goal:
                    return path + [neighbor]
                else:
                    heapq.heappush(priority_queue, (heuristic(neighbor, goal), neighbor, path + [neighbor]))
    return None

def a_star(graph, start, goal):
    open_list = [(heuristic(start, goal), 0, start, [start])]
    while open_list:
        _, cost_so_far, vertex, path = heapq.heappop(open_list)
        for neighbor, edge_cost in graph[vertex]:
            if neighbor not in path:
                new_cost = cost_so_far + edge_cost
                if neighbor == goal:
                    return path + [neighbor]
                else:
                    heapq.heappush(open_list, (new_cost + heuristic(neighbor, goal), new_cost, neighbor, path + [neighbor]))
    return None

import random

def custom_search_1(graph, start, goal):
    current = start
    path = [start]
    visited = set([start])
    while current != goal:
        neighbors = [n for n, _ in graph[current] if n not in visited]
        if not neighbors:
            if len(path) > 1:
                path.pop()
                current = path[-1]
            else:
                return None
        else:
            next_node = random.choice(neighbors)
            path.append(next_node)
            visited.add(next_node)
            current = next_node
    return path

def custom_search_2(graph, start, goal):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start, [start])]
    while priority_queue:
        current_distance, current_node, current_path = heapq.heappop(priority_queue)
        if current_node == goal:
            return current_path
        if current_distance > distances[current_node]:
            continue
        for neighbor, edge_cost in graph[current_node]:
            distance = current_distance + edge_cost
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor, current_path + [neighbor]))
    return None



start = 'A'
print("DFS:", dfs(graph, start, goal))
print("BFS:", bfs(graph, start, goal))
print("GBFS:", gbfs(graph, start, goal))
print("A*:", a_star(graph, start, goal))
print("Custom Search 1:", custom_search_1(graph, start, goal))
print("Custom Search 2:", custom_search_2(graph, start, goal))    