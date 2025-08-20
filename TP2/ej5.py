graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],  # pared hacia D
    'D': [],     # rodeado de paredes hacia C y E
    'E': ['D'],  # pared desde D
    'G': ['I', 'P'],
    'I': ['G', 'Q'],  # W es bloqueado hacia K
    'W': ['R'],        # pared hacia K
    'K': ['M'],        # pared desde W
    'M': ['K', 'N'],
    'N': ['M'],
    'P': ['G', 'Q'],
    'Q': ['P', 'I', 'R'],
    'R': ['Q', 'W', 'T'],
    'T': ['R'],        # pared hacia F
    'F': []            # objetivo
}

coords = {
    'A': (0,0), 'B': (1,0),
    'C': (0,1), 'D': (1,1), 'E': (2,1),
    'G': (0,2), 'I': (1,2), 'W': (2,2), 'K': (3,2), 'M': (4,2), 'N': (5,2),
    'P': (0,3), 'Q': (1,3), 'R': (2,3), 'T': (3,3), 'F': (4,3)
}

def manhattan(casilla):
    x1, y1 = coords[casilla]
    x2, y2 = coords['F']
    return abs(x1 - x2) + abs(y1 - y2)

def dfs(start, goal, graph):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in sorted(graph[node], reverse=True):  # alfabético
                stack.append((neighbor, path + [neighbor]))
    return None

import heapq

def greedy(start, goal, graph):
    heap = [(manhattan(start), start, [start])]
    visited = set()
    while heap:
        _, node, path = heapq.heappop(heap)
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in sorted(graph[node]):
                heapq.heappush(heap, (manhattan(neighbor), neighbor, path + [neighbor]))
    return None

def a_star(start, goal, graph):
    heap = [(manhattan(start), 0, start, [start])]  # (f = g + h, g, node, path)
    visited = {}
    cost_map = {'W': 30}  # resto costo 1

    while heap:
        f, g, node, path = heapq.heappop(heap)
        if node == goal:
            return path
        if node not in visited or g < visited[node]:
            visited[node] = g
            for neighbor in sorted(graph[node]):
                g_new = g + cost_map.get(neighbor, 1)
                f_new = g_new + manhattan(neighbor)
                heapq.heappush(heap, (f_new, g_new, neighbor, path + [neighbor]))
    return None

print("DFS:", dfs('I','F',graph))
print("Greedy:", greedy('I','F',graph))
print("A*:", a_star('I','F',graph))
