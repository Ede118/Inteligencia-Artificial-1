graph = {               #definimos los vecinos del grafico
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'K'],    
    'D': ['B','M'],     
    'E': ['N'],         
    'G': ['I', 'P'],
    'I': ['G', 'Q', 'W'],  
    'W': ['I', 'K'],  
    'K': ['C', 'M', 'T', 'W'],     
    'M': ['D', 'F', 'K', 'N'],
    'N': ['E','M'],
    'P': ['G', 'Q'],
    'Q': ['I', 'P', 'R'],
    'R': ['Q', 'T'],
    'T': ['K','R'],        
    'F': ['N']            
}

#asignamos coordenadas a las casillas para poder calcular la distancia Manhattan
coords = {                  
    'A': (0,0), 'B': (1,0),
    'C': (0,1), 'D': (1,1), 'E': (2,1),
    'G': (0,2), 'I': (1,2), 'W': (2,2), 'K': (3,2), 'M': (4,2), 'N': (5,2),
    'P': (0,3), 'Q': (1,3), 'R': (2,3), 'T': (3,3), 'F': (4,3)
}

#calculo de distancia manhattan
def manhattan(casilla):
    x1, y1 = coords[casilla]
    x2, y2 = coords['F']
    return abs(x1 - x2) + abs(y1 - y2)

#Busqueda Primero en profundidad
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

#Busqueda Avara
def greedy(start, goal, graph):
    heap = [(manhattan(start), 0, start, [start])]
    visited = {}
    while heap:
        f, g, node, path = heapq.heappop(heap)
        if node == goal:
            return path
        if node not in visited or g < visited[node]:
            visited[node] = g
            for neighbor in sorted(graph[node]):
                g_new = g + 1   # cada paso cuesta 1, incluso W 
                f_new = g_new + manhattan(neighbor) #solo tiene en cuenta la distancia más corta hasta el obj
                heapq.heappush(heap, (f_new, g_new, neighbor, path + [neighbor]))
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
                g_new = g + cost_map.get(neighbor, 1) #cuenta el costo del camino y la menor distancia hasta el obj
                f_new = g_new + manhattan(neighbor)
                heapq.heappush(heap, (f_new, g_new, neighbor, path + [neighbor]))
    return None

#Calculamos los costos de cada camino
def path_cost(path):
    cost_map = {'W': 30}  # resto 1
    total = 0
    for node in path[1:]:  # no contamos la casilla inicial
        total += cost_map.get(node, 1)
    return total

dfs_path = dfs('I','F',graph)
greedy_path = greedy('I','F',graph)
astar_path = a_star('I','F',graph)

print("\nPrimero en Profundidad:", dfs_path, "\nCosto:", path_cost(dfs_path), "\nLargo del camino:", len(dfs_path)-1)
print("\nGreedy:", greedy_path, "\nCosto:", path_cost(greedy_path), "\nLargo del camino:", len(greedy_path)-1)
print("\nA*:", astar_path, "\nCosto:", path_cost(astar_path), "\nLargo del camino:", len(astar_path)-1)
