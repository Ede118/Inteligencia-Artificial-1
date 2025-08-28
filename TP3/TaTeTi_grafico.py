import pygame
import sys
import math
import random
import threading
import time

# ----------------- Lógica del Juego y de la IA (sin cambios) -----------------

def new_board(): 
    return [' '] * 9

def available_moves(b): 
    return [i for i, c in enumerate(b) if c == ' ']

def place(b, i, mark): b[i] = mark

def winner(b):
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for i,j,k in lines:
        if b[i] != ' ' and b[i] == b[j] == b[k]: return b[i]
    return None

def is_draw(b): 
    return winner(b) is None and all(c != ' ' for c in b)

def copy_board(b): 
    return b[:]

def random_policy_move(b, player):
    for i in available_moves(b):
        bb = copy_board(b); place(bb, i, player)
        if winner(bb) == player: return i
    opp = 'O' if player == 'X' else 'X'
    for i in available_moves(b):
        bb = copy_board(b); place(bb, i, opp)
        if winner(bb) == opp: return i
    return random.choice(available_moves(b)) if available_moves(b) else -1

def simulate_from_move(b, move, ai, hu):
    bb = copy_board(b); place(bb, move, ai)
    w = winner(bb)
    if w == ai: return 1
    if is_draw(bb): return 0
    turn = hu
    while True:
        m = random_policy_move(bb, turn)
        if m == -1: return 0 # No hay más movimientos
        place(bb, m, turn)
        w = winner(bb)
        if w == ai: return 1
        if w == hu: return -1
        if is_draw(bb): return 0
        turn = ai if turn == hu else hu

def estimated_value(b, move, ai, hu, rollouts=40):
    s = 0
    for _ in range(rollouts): s += simulate_from_move(b, move, ai, hu)
    return s / rollouts

def Recocido(b, ai, hu, T0=10.0, Tf=0.1, alpha=0.95, L=20, rollouts=40):
    empties = available_moves(b)
    for i in empties:
        bb = copy_board(b); place(bb, i, ai)
        if winner(bb) == ai: return i
    for i in empties:
        bb = copy_board(b); place(bb, i, hu)
        if winner(bb) == hu: return i
    if not empties: return -1
    current = random.choice(empties)
    best = current
    cur_val = estimated_value(b, current, ai, hu, rollouts=rollouts)
    best_val = cur_val
    T = T0
    while T > Tf and len(empties) > 1:
        for _ in range(L):
            neighbor = random.choice([m for m in empties if m != current])
            neigh_val = estimated_value(b, neighbor, ai, hu, rollouts=rollouts)
            dE = -(neigh_val - cur_val)
            if dE < 0 or random.random() < math.exp(-dE / T):
                current, cur_val = neighbor, neigh_val
                if cur_val > best_val:
                    best, best_val = current, neigh_val
        T *= alpha
    return best

# ----------------- Interfaz Gráfica con Pygame -----------------

class TicTacToePygame:
    def __init__(self):
        pygame.init()
        # --- Constantes de la ventana ---
        self.WIDTH, self.HEIGHT = 450, 550
        self.LINE_WIDTH = 10
        self.BOARD_ROWS, self.BOARD_COLS = 3, 3
        self.SQUARE_SIZE = self.WIDTH // self.BOARD_COLS
        self.CIRCLE_RADIUS = self.SQUARE_SIZE // 3
        self.CIRCLE_WIDTH = 15
        self.CROSS_WIDTH = 25
        # --- Colores ---
        self.BG_COLOR = (240, 230, 210)
        self.LINE_COLOR = (50, 50, 50)
        self.CIRCLE_COLOR = (239, 83, 80) # Rojo
        self.CROSS_COLOR = (66, 165, 245) # Azul
        # --- Fuentes ---
        self.FONT = pygame.font.SysFont('Arial', 40, bold=True)
        # --- Configuración de la ventana ---
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Ta-te-ti con IA (Pygame)')
        self.restart_game()

    def restart_game(self):
        self.board = new_board()
        self.human = random.choice(['X', 'O'])
        self.ai = 'O' if self.human == 'X' else 'X'
        self.turn = 'X'
        self.game_over = False
        self.winner = None
        self.ai_thinking = False
        if self.turn == self.ai:
            self.trigger_ai_move()

    def draw_lines(self):
        self.screen.fill(self.BG_COLOR)
        # Líneas horizontales
        pygame.draw.line(self.screen, self.LINE_COLOR, (0, self.SQUARE_SIZE), (self.WIDTH, self.SQUARE_SIZE), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (0, 2 * self.SQUARE_SIZE), (self.WIDTH, 2 * self.SQUARE_SIZE), self.LINE_WIDTH)
        # Líneas verticales
        pygame.draw.line(self.screen, self.LINE_COLOR, (self.SQUARE_SIZE, 0), (self.SQUARE_SIZE, self.WIDTH), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (2 * self.SQUARE_SIZE, 0), (2 * self.SQUARE_SIZE, self.WIDTH), self.LINE_WIDTH)

    def draw_figures(self):
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                mark = self.board[row * 3 + col]
                if mark == 'O':
                    center = (int(col * self.SQUARE_SIZE + self.SQUARE_SIZE / 2), int(row * self.SQUARE_SIZE + self.SQUARE_SIZE / 2))
                    pygame.draw.circle(self.screen, self.CIRCLE_COLOR, center, self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)
                elif mark == 'X':
                    x1 = col * self.SQUARE_SIZE + self.SQUARE_SIZE / 4
                    y1 = row * self.SQUARE_SIZE + self.SQUARE_SIZE / 4
                    pygame.draw.line(self.screen, self.CROSS_COLOR, (x1, y1), (x1 + self.SQUARE_SIZE/2, y1 + self.SQUARE_SIZE/2), self.CROSS_WIDTH)
                    pygame.draw.line(self.screen, self.CROSS_COLOR, (x1, y1 + self.SQUARE_SIZE/2), (x1 + self.SQUARE_SIZE/2, y1), self.CROSS_WIDTH)
    
    def draw_status(self):
        if self.game_over:
            if self.winner:
                # Modificación clave aquí
                if self.winner == self.human:
                    message = "¡Ganaste!(Click para reiniciar)"
                else:
                    message = "Perdiste.(Click para reiniciar)"
            else:
                message = "Empate!(Click para reiniciar)"
        elif self.ai_thinking:
            message = "IA está pensando..."
        else:
            message = f"Sos '{self.human}'. Turno de '{self.turn}'"
            
        text = self.FONT.render(message, True, self.LINE_COLOR)
        text_rect = text.get_rect(center=(self.WIDTH/2, self.HEIGHT - 50))
        self.screen.blit(text, text_rect)
    
    def trigger_ai_move(self):
        self.ai_thinking = True
        # Inicia el cálculo de la IA en un hilo separado para no congelar la ventana
        threading.Thread(target=self.ai_move_threaded, daemon=True).start()

    def ai_move_threaded(self):
        time.sleep(0.5) # Pequeña pausa para que se vea el "pensando..."
        move = Recocido(self.board, self.ai, self.human)
        # Cuando termina, el resultado se manejará en el bucle principal
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'move': move}))

    def run(self):
        running = True
        while running:
            self.draw_lines()
            self.draw_figures()
            self.draw_status()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if self.turn == self.human and not self.ai_thinking:
                        mouseX, mouseY = event.pos
                        if mouseY < self.WIDTH: # Asegurarse de que el click es en el tablero
                            clicked_row = int(mouseY // self.SQUARE_SIZE)
                            clicked_col = int(mouseX // self.SQUARE_SIZE)
                            square_index = clicked_row * 3 + clicked_col
                            
                            if self.board[square_index] == ' ':
                                place(self.board, square_index, self.human)
                                # Lógica para determinar el estado del juego
                                self.winner = winner(self.board)
                                if self.winner or is_draw(self.board):
                                    self.game_over = True
                                else:
                                    self.turn = self.ai
                                    self.trigger_ai_move()
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    self.restart_game()

                # Evento personalizado que se dispara cuando la IA termina de pensar
                if event.type == pygame.USEREVENT:
                    self.ai_thinking = False
                    ai_move = event.move
                    if ai_move != -1 and self.board[ai_move] == ' ':
                        place(self.board, ai_move, self.ai)
                        # Lógica para determinar el estado del juego
                        self.winner = winner(self.board)
                        if self.winner or is_draw(self.board):
                            self.game_over = True
                        else:
                            self.turn = self.human

            pygame.display.update()

# ----------------- Función Principal -----------------
if __name__ == "__main__":
    game = TicTacToePygame()
    game.run()