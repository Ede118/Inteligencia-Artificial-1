import pygame
import sys
import random

##########################################
# --- Configuración de la simulación --- #
###########################################

GRID_WIDTH = 100
GRID_HEIGHT = 80
CELL_SIZE = 8
FPS = 120

########################
#     Colores y UI     #
########################

ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)
GRID_LINE_COLOR = (50, 50, 50)

UI_BG = (30, 30, 30)
BTN_BG = (60, 60, 60)
BTN_BG_HOVER = (90, 90, 90)
BTN_TEXT = (230, 230, 230)
UI_BAR_HEIGHT = 48
PADDING = 8
BTN_W, BTN_H = 100, 32
BTN_GAP = 12

########################################
#     Inicialización de Pygame     #
########################################

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 22)

SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + UI_BAR_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de la Vida")
clock = pygame.time.Clock()

########################################
#     Funciones de la simulación     #
########################################

def crear_grilla_vacia():
    """Crea una grilla con todas las celdas muertas (0)."""
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def crear_grilla_aleatoria():
    """Crea una grilla con celdas vivas y muertas de forma aleatoria."""
    return [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    """Dibuja las celdas vivas de la cuadrícula."""
    screen.fill(DEAD_COLOR)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, ALIVE_COLOR, rect)

def draw_grid_lines():
    """Dibuja las líneas de la cuadrícula para una mejor visualización."""
    for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRID_LINE_COLOR, (x, 0), (x, GRID_HEIGHT * CELL_SIZE))
    for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, y), (GRID_WIDTH * CELL_SIZE, y))

def contar_vecinos(grid, x, y):
    """Cuenta el número de vecinos vivos para una celda dada."""
    total = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = (x + dx) % GRID_WIDTH
            ny = (y + dy) % GRID_HEIGHT
            total += grid[ny][nx]
    return total

def actualizar_grilla(grid):
    """Crea una nueva grilla basada en las reglas del Juego de la Vida."""
    new_grid = crear_grilla_vacia()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            vecinos = contar_vecinos(grid, x, y)
            if grid[y][x] == 1:
                if vecinos in [2, 3]:
                    new_grid[y][x] = 1
            else:
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
    """Dibuja un botón en la pantalla."""
    hovered = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, BTN_BG_HOVER if hovered else BTN_BG, rect, border_radius=6)
    text_surf = font.render(label, True, BTN_TEXT)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_ui(mouse_pos, sim_running, generation):
    """Dibuja la barra de interfaz de usuario con botones e información."""
    ui_rect = pygame.Rect(0, GRID_HEIGHT * CELL_SIZE, SCREEN_WIDTH, UI_BAR_HEIGHT)
    pygame.draw.rect(screen, UI_BG, ui_rect)
    info = f"Estado: {'RUN' if sim_running else 'PAUSE'} | Generación: {generation}"
    info_surf = font.render(info, True, BTN_TEXT)
    screen.blit(info_surf, (SCREEN_WIDTH - info_surf.get_width() - PADDING,
                            GRID_HEIGHT * CELL_SIZE + (UI_BAR_HEIGHT - info_surf.get_height()) // 2))

    draw_button(start_btn, "Start (Space)", mouse_pos)
    draw_button(stop_btn, "Stop", mouse_pos)
    draw_button(reset_btn, "Reset (R)", mouse_pos)

def reset_simulation():
    """Limpia la grilla y la reinicia."""
    global grid, generation
    grid = crear_grilla_vacia()
    generation = 0


########################################
#     Inicialización del Juego     #
########################################

grid = crear_grilla_vacia()
start_btn, stop_btn, reset_btn = make_button_rects()
sim_running = False
generation = 0

# --- Bucle principal del juego ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Clic inicial del ratón
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start_btn.collidepoint(event.pos):
                sim_running = True
            elif stop_btn.collidepoint(event.pos):
                sim_running = False
            elif reset_btn.collidepoint(event.pos):
                sim_running = False
                reset_simulation()
        
        # Atajos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sim_running = not sim_running
            elif event.key == pygame.K_r:
                sim_running = False
                reset_simulation()
            elif event.key == pygame.K_a: # Atajo para la grilla aleatoria
                sim_running = False
                grid = crear_grilla_aleatoria()
                generation = 0
            elif event.key == pygame.K_q: # Atajo para salir
                running = False
                

    # Lógica para dibujar manteniendo el clic
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0] and not sim_running: # El botón 0 es el clic izquierdo
        mouse_x, mouse_y = mouse_pos
        if mouse_y < GRID_HEIGHT * CELL_SIZE:
            grid_x = mouse_x // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            grid[grid_y][grid_x] = 1

    # Lógica de la simulación
    if sim_running:
        grid = actualizar_grilla(grid)
        generation += 1

    # Dibujo
    draw_grid(grid)
    draw_grid_lines()
    draw_ui(mouse_pos, sim_running, generation)
    
    # Actualiza la pantalla
    pygame.display.flip()
    
    # Controla la velocidad
    clock.tick(FPS)

# Salida
pygame.quit()
sys.exit()
