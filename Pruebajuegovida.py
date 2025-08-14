import pygame
import sys

##########################################
# --- Configuración de la simulación --- #
###########################################

GRID_WIDTH = 100
GRID_HEIGHT = 80
CELL_SIZE = 8
FPS = 1

########################
#     Colores y UI     #
########################

GREEN = (0, 255, 0)  # Celdas 'vivas'
WHITE = (255, 255, 255)        # Celdas 'muertas'

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
pygame.display.set_caption("Juego de la Vida")
clock = pygame.time.Clock()

# Estado inicial
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] 
#primero todas las celulas estan muertas

########################################
#        Clases y Funciones            #
########################################

#dibujo del tablero
def draw_grid(grid):
    """Dibuja toda la cuadricula en la pantalla"""
    screen.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
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
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            vecinos = contar_vecinos(grid, x, y)
            if grid[y][x] == 1:         #si la celula ya esta viva revisa la condicion de supervivencia
                if vecinos in [2, 3]:
                    new_grid[y][x] = 1
            else:                       #si la celula esta muerta la hace nacer si los vecinos son igual a 3
                if vecinos == 3:
                    new_grid[y][x] = 1
    return new_grid

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
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            grid[y][x] = 0

########################################
#        Inicialización del Juego     #
########################################

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
# Botones y Estado de ejecución
start_btn, stop_btn, reset_btn = make_button_rects()
sim_running = False


# --- Bucle principal del juego ---
running = True
while running:
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
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE
                    grid[grid_y][grid_x] = 1
        # Atajos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sim_running = not sim_running
            elif event.key == pygame.K_r:
                sim_running = False
                reset_simulation()

    grid = actualizar_grilla(grid)
    draw_grid(grid)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()