import pygame
import sys

##########################################
# --- Configuración de la simulación --- #
###########################################

GRID_WIDTH = 200
GRID_HEIGHT = 150
CELL_SIZE = 4
FPS = 240

########################
#     Colores y UI     #
########################

WHITE = (0, 0, 0)               # Celdas 'blancas'
BLACK = (255, 255, 255)         # Celdas 'negras'
ANT_COLOR = (255, 0, 0)         # Color de la hormiga

UI_BG = (30, 30, 30)            # Fondo de la UI
BTN_BG = (60, 60, 60)           # Fondo de los botones
BTN_BG_HOVER = (90, 90, 90)     # Fondo de los botones al pasar el ratón
BTN_TEXT = (230, 230, 230)      # Texto de los botones
UI_BAR_HEIGHT = 48              # Altura de la barra de UI
PADDING = 8                     # Espacio entre elementos de la UI
BTN_W, BTN_H = 100, 32          # Ancho y alto de los botones
BTN_GAP = 12                    # Espacio entre botones


########################################
#        Inicialización de Pygame     #
########################################


pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 22)

SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + UI_BAR_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hormiga de Langton (Múltiples Hormigas)")
clock = pygame.time.Clock()


########################################
#        Clases y Funciones            #
########################################


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

def make_button_rects():
    """Crea los rects de botones alineados en la barra inferior."""
    x = PADDING
    y = GRID_HEIGHT * CELL_SIZE + (UI_BAR_HEIGHT - BTN_H) // 2
    start_rect = pygame.Rect(x, y, BTN_W, BTN_H)
    x += BTN_W + BTN_GAP
    stop_rect = pygame.Rect(x, y, BTN_W, BTN_H)
    x += BTN_W + BTN_GAP
    reset_rect = pygame.Rect(x, y, BTN_W, BTN_H)
    return start_rect, stop_rect, reset_rect


def draw_button(rect, label, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, BTN_BG_HOVER if hovered else BTN_BG, rect, border_radius=6)
    text_surf = font.render(label, True, BTN_TEXT)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def draw_ui(mouse_pos, sim_running, ants_count):
    """Dibuja la barra y los botones."""
    ui_rect = pygame.Rect(0, GRID_HEIGHT * CELL_SIZE, SCREEN_WIDTH, UI_BAR_HEIGHT)
    pygame.draw.rect(screen, UI_BG, ui_rect)

    # Info al costado
    info = f"Estado: {'RUN' if sim_running else 'PAUSE'}  |  Hormigas: {ants_count}"
    info_surf = font.render(info, True, BTN_TEXT)
    screen.blit(info_surf, (SCREEN_WIDTH - info_surf.get_width() - PADDING,
                            GRID_HEIGHT * CELL_SIZE + (UI_BAR_HEIGHT - info_surf.get_height()) // 2))

    # Botones
    draw_button(start_btn, "Start", mouse_pos)
    draw_button(stop_btn, "Stop", mouse_pos)
    draw_button(reset_btn, "Reset (R)", mouse_pos)


def reset_simulation():
    """Limpia la grilla y las hormigas."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            grid[y][x] = 0
    ants.clear()

########################################
#        Inicialización del Juego     #
########################################


grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
ants = []  # Lista para almacenar los objetos de las hormigas

# Botones y Estado de ejecución
start_btn, stop_btn, reset_btn = make_button_rects()
sim_running = False


# --- Bucle principal del juego ---
running = True
while running:
    
    mouse_pos = pygame.mouse.get_pos() # Posición del ratón

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Click izquierdo del ratón
            # Si el click es en el "Start" botón empieza el juego
            if start_btn.collidepoint(event.pos):
                sim_running = True
            
            # Si el click es en el "Stop" botón para el juego
            elif stop_btn.collidepoint(event.pos):
                sim_running = False
            
            # Si el click es en el "Reset" botón reinicia la simulación
            elif reset_btn.collidepoint(event.pos):
                sim_running = False
                reset_simulation()

            # Si el click es dentro del área del grid, agregar hormiga
            else:
                mouse_x, mouse_y = event.pos
                if mouse_y < GRID_HEIGHT * CELL_SIZE:  # <-- solo dentro del grid
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE
                    ants.append(Ant(grid_x, grid_y))

        # Atajos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sim_running = not sim_running
            elif event.key == pygame.K_r:
                sim_running = False
                reset_simulation()

    # --- Lógica de la hormiga ---
        if sim_running:
            for ant in ants:
                current_cell_color = grid[ant.x][ant.y]
                if current_cell_color == 1:
                    ant.turn_right()
                    grid[ant.x][ant.y] = 0
                else:
                    ant.turn_left()
                    grid[ant.x][ant.y] = 1
                ant.move()


    # --- Dibujo ---
    draw_grid(grid)
    
    # Dibuja todas las hormigas
    for ant in ants:
        ant_rect = pygame.Rect(ant.x * CELL_SIZE, ant.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, ANT_COLOR, ant_rect)

    # UI
    draw_ui(mouse_pos, sim_running, len(ants))
    
    # Actualiza la pantalla
    pygame.display.flip()
    
    # Controla la velocidad de la simulación
    clock.tick(FPS)

# --- Salida ---
pygame.quit()
sys.exit()