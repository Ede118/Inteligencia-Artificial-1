import pygame
import sys

# --- Configuración de la simulación ---
GRID_WIDTH = 100
GRID_HEIGHT = 80
CELL_SIZE = 8
FPS = 1

# --- Colores ---
GREEN = (0, 255, 0)  # Celdas 'vivas'
WHITE = (255, 255, 255)        # Celdas 'muertas'

# --- Inicialización de Pygame ---
pygame.init()
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de la Vida")
clock = pygame.time.Clock()

# Estado inicial
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] 
#primero todas las celulas estan muertas

#dibujo del tablero
def draw_grid(grid):
    screen.fill(WHITE)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 1:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GREEN, rect)            

#contar vecinos
def contar_vecinos(grid, x, y):
    total = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = (x + dx) % GRID_WIDTH
            ny = (y + dy) % GRID_HEIGHT
            total += grid[ny][nx]
    return total
#usa % para envolver ls bordes

#Actualizacion de la cuadricula
def actualizar_grilla(grid):
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            vecinos = contar_vecinos(grid, x, y)
            if grid[x][y] == 1:         #si la celula ya esta viva revisa la condicion de supervivencia
                if vecinos in [2, 3]:
                    new_grid[x][y] = 1
            else:                       #si la celula esta muerta la hace nacer si los vecinos son igual a 3
                if vecinos == 3:
                    new_grid[x][y] = 1
    return new_grid

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            grid_x = mouse_x // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            if grid[grid_x][grid_y] == 0:
                grid[grid_x][grid_y] = 1  # Celda muerta → viva
            else:
                grid[grid_x][grid_y] = 0  # Celda viva → muerta

    grid = actualizar_grilla(grid)
    draw_grid(grid)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()