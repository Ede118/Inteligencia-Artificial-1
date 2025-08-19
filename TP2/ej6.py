import tkinter as tk
from tkinter import messagebox
import heapq

class Node:
    """Clase para representar un nodo en la cuadrícula de búsqueda."""
    def __init__(self, row, col, parent=None):
        self.row = row
        self.col = col
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash((self.row, self.col))

def heuristic(node, end_node):
    """Calcula la heurística de distancia de Manhattan."""
    return abs(node.row - end_node.row) + abs(node.col - end_node.col)

def astar(grid, start, end):
    """El algoritmo de búsqueda A* corregido."""
    start_node = Node(start.row, start.col)
    end_node = Node(end.row, end.col)

    open_list = [start_node]
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)
        
        if current_node in closed_set:
            continue
        
        closed_set.add(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append((current.row, current.col))
                current = current.parent
            return path[::-1]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_row, neighbor_col = current_node.row + dr, current_node.col + dc

            if 0 <= neighbor_row < 20 and 0 <= neighbor_col < 20 and grid.get((neighbor_row, neighbor_col)) != 1:
                neighbor = Node(neighbor_row, neighbor_col, current_node)

                if neighbor in closed_set:
                    continue

                neighbor.g = current_node.g + 1
                neighbor.h = heuristic(neighbor, end_node)
                neighbor.f = neighbor.g + neighbor.h
                
                heapq.heappush(open_list, neighbor)

    return None

class PathfindingGUI:
    """Clase para la interfaz gráfica."""
    def __init__(self, master, rows, cols):
        self.master = master
        master.title("Buscador de Caminos A*")

        self.rows = rows
        self.cols = cols
        self.grid = {}
        self.start = None
        self.end = None
        self.path = []

        self.buttons = {}
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(master, text="", width=2, height=1,
                                   command=lambda row=r, col=c: self.cell_clicked(row, col))
                button.grid(row=r, column=c)
                self.buttons[(r, c)] = button
                self.grid[(r, c)] = 0

        find_button = tk.Button(master, text="Encontrar Camino", command=self.find_path)
        find_button.grid(row=rows, column=0, columnspan=cols)

        reset_button = tk.Button(master, text="Reiniciar", command=self.reset_grid)
        reset_button.grid(row=rows + 1, column=0, columnspan=cols)

    def cell_clicked(self, row, col):
        """Maneja los clics en las celdas para establecer inicio, fin o paredes."""
        if self.grid.get((row, col)) == 2:
            self.grid[(row, col)] = 0
            self.buttons[(row, col)].config(text="", bg="white")
            self.start = None
        elif self.grid.get((row, col)) == 3:
            self.grid[(row, col)] = 0
            self.buttons[(row, col)].config(text="", bg="white")
            self.end = None
        elif self.start is None:
            self.start = Node(row, col)
            self.grid[(row, col)] = 2
            self.buttons[(row, col)].config(text="S", bg="lightgreen")
        elif self.end is None:
            self.end = Node(row, col)
            self.grid[(row, col)] = 3
            self.buttons[(row, col)].config(text="E", bg="lightblue")
        else:
            if self.grid[(row, col)] == 1:
                self.grid[(row, col)] = 0
                self.buttons[(row, col)].config(bg="white")
            else:
                self.grid[(row, col)] = 1
                self.buttons[(row, col)].config(bg="black")

    def find_path(self):
        """Inicia la búsqueda A* y muestra el camino."""
        if not self.start or not self.end:
            messagebox.showerror("Error", "Por favor, selecciona un punto de inicio y uno de fin.")
            return

        path = astar(self.grid, self.start, self.end)

        self._reset_path_display()

        if path:
            for row, col in path:
                if (row, col) != (self.start.row, self.start.col) and (row, col) != (self.end.row, self.end.col):
                    self.buttons[(row, col)].config(bg="yellow")
        else:
            messagebox.showinfo("Información", "No se encontró un camino.")

    def _reset_path_display(self):
        """Reinicia el color de las celdas del camino."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[(r, c)] == 0:
                    self.buttons[(r, c)].config(bg="white")

    def reset_grid(self):
        """Reinicia la cuadrícula a su estado inicial."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[(r, c)] = 0
                self.buttons[(r, c)].config(text="", bg="white")
        self.start = None
        self.end = None
        self._reset_path_display()

if __name__ == "__main__":
    rows = 20
    cols = 20
    root = tk.Tk()
    gui = PathfindingGUI(root, rows, cols)
    root.mainloop()