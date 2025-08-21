import tkinter as tk
import heapq

# --- Definición del grafo y coordenadas ---
graph = {
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

coords = {
    'A': (3,3), 'B': (3,4),
    'C': (2,3), 'D': (2,4), 'E': (2,5),
    'G': (1,0), 'I': (1,1), 'W': (1,2), 'K': (1,3), 'M': (1,4), 'N': (1,5),
    'P': (0,0), 'Q': (0,1), 'R': (0,2), 'T': (0,3), 'F': (0,4)
}

# Paredes (pares de casillas donde no hay conexión)
walls = {("C","D"), ("D","E"), ("W","R"), ("T","F")}

# --- Algoritmos de búsqueda ---
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
            for neighbor in sorted(graph[node], reverse=True):
                stack.append((neighbor, path + [neighbor]))
    return None

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
    heap = [(manhattan(start), 0, start, [start])]
    visited = {}
    cost_map = {'W': 30}
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

# --- Interfaz gráfica ---
CELL = 60
ROWS, COLS = 6, 6   # dimensiones de la grilla

def draw_board(path=None):
    canvas.delete("all")

    # Dibujar cuadriculado
    for r in range(ROWS):
        for c in range(COLS):
            x1, y1 = c*CELL, r*CELL
            x2, y2 = x1+CELL, y1+CELL
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

    # Dibujar nodos
    for node, (x,y) in coords.items():
        x1, y1 = x*CELL, y*CELL
        x2, y2 = x1+CELL, y1+CELL

        color = "white"
        if node == "I" or node == "F":
            color = "yellow"
        if path and node in path:
            color = "lightgreen"

        canvas.create_rectangle(x1,y1,x2,y2, fill=color, outline="black")
        canvas.create_text((x1+x2)//2, (y1+y2)//2, text=node)

    # Dibujar paredes
    for (n1,n2) in walls:
        if n1 in coords and n2 in coords:
            x1,y1 = coords[n1]
            x2,y2 = coords[n2]
            if x1==x2: # pared horizontal
                cx = x1*CELL
                cy = max(y1,y2)*CELL
                canvas.create_rectangle(cx,cy-5,cx+CELL,cy+5,fill="red",outline="red")
            else: # pared vertical
                cx = max(x1,x2)*CELL
                cy = y1*CELL
                canvas.create_rectangle(cx-5,cy,cx+5,cy+CELL,fill="red",outline="red")

def run_algorithm(algo):
    if algo=="DFS":
        path = dfs("I","F",graph)
    elif algo=="Greedy":
        path = greedy("I","F",graph)
    else:
        path = a_star("I","F",graph)
    draw_board(path)

# --- Ventana Tkinter ---
root = tk.Tk()
root.title("Búsquedas en tablero")

canvas = tk.Canvas(root, width=COLS*CELL, height=ROWS*CELL, bg="white")
canvas.pack()

frame = tk.Frame(root)
frame.pack()

tk.Button(frame,text="DFS",command=lambda: run_algorithm("DFS")).pack(side=tk.LEFT)
tk.Button(frame,text="Greedy",command=lambda: run_algorithm("Greedy")).pack(side=tk.LEFT)
tk.Button(frame,text="A*",command=lambda: run_algorithm("A*")).pack(side=tk.LEFT)

draw_board()
root.mainloop()
