import pygame
import sys

# --- Configuración de la simulación ---
GRID_WIDTH = 200
GRID_HEIGHT = 150
CELL_SIZE = 4
FPS = 240

# --- Colores ---
WHITE = (0, 0, 0)  # Celdas 'blancas'
BLACK = (255, 255, 255)        # Celdas 'negras'
ANT_COLOR = (255, 0, 0)  # Color de la hormiga

# --- Inicialización de Pygame ---
pygame.init()
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hormiga de Langton (Múltiples Hormigas)")
clock = pygame.time.Clock()

# --- Clases y funciones ---
class Ant:
    """Representa la hormiga con su posición y dirección."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # 0: arriba, 1: derecha, 2: abajo, 3: izquierda
        self.direction = 0

    def turn_right(self):
        """Gira la hormiga 90 grados a la derecha."""
        self.direction = (self.direction + 1) % 4

    def turn_left(self):
        """Gira la hormiga 90 grados a la izquierda."""
        self.direction = (self.direction - 1 + 4) % 4

    def move(self):
        """Mueve la hormiga un paso en su dirección actual."""
        if self.direction == 0:  # Arriba
            self.y -= 1
        elif self.direction == 1:  # Derecha
            self.x += 1
        elif self.direction == 2:  # Abajo
            self.y += 1
        elif self.direction == 3:  # Izquierda
            self.x -= 1
        
        # Envuelve la posición si sale de los límites de la cuadrícula
        self.x = self.x % GRID_WIDTH
        self.y = self.y % GRID_HEIGHT
        # Asegura que las coordenadas sean no negativas
        if self.x < 0: self.x += GRID_WIDTH
        if self.y < 0: self.y += GRID_HEIGHT


def draw_grid(grid):
    """Dibuja toda la cuadrícula en la pantalla."""
    screen.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[x][y] == 1:  # Si la celda está 'negra'
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect)

# --- Inicialización de la simulación ---
grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
ants = []  # Lista para almacenar los objetos de las hormigas

# --- Bucle principal del juego ---
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Convierte las coordenadas del clic del ratón en coordenadas de la cuadrícula
            mouse_x, mouse_y = event.pos
            grid_x = mouse_x // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            # Añade una nueva hormiga en la posición del clic
            ants.append(Ant(grid_x, grid_y))

    # --- Lógica de la hormiga ---
    for ant in ants:
        # Obtiene el color de la celda actual
        current_cell_color = grid[ant.x][ant.y]

        if current_cell_color == 1:  # Si la celda es negra
            ant.turn_right()
            grid[ant.x][ant.y] = 0  # Cambia a blanco
        else:  # Si la celda es blanca
            ant.turn_left()
            grid[ant.x][ant.y] = 1  # Cambia a negro

        ant.move()

    # --- Dibujo ---
    draw_grid(grid)
    
    # Dibuja todas las hormigas
    for ant in ants:
        ant_rect = pygame.Rect(ant.x * CELL_SIZE, ant.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, ANT_COLOR, ant_rect)

    # Actualiza la pantalla
    pygame.display.flip()
    
    # Controla la velocidad de la simulación
    clock.tick(FPS)

# --- Salida ---
pygame.quit()
sys.exit()