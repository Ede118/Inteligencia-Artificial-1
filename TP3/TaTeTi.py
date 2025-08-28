# Ta-te-ti con IA por Recocido Simulado (Simulated Annealing)

import math
import random

# ----------------- Tablero y reglas -----------------

def new_board():
    return [' '] * 9

def print_board(b):
    print()
    for r in range(3):
        row = b[3*r:3*r+3]
        print(' ' + ' | '.join(c if c != ' ' else str(3*r+i+1) for i, c in enumerate(row)))
        if r < 2: print("---+---+---")
    print()

def available_moves(b):
    return [i for i, c in enumerate(b) if c == ' ']

def place(b, i, mark):
    b[i] = mark

def winner(b):
    lines = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,6),(1,4,7),(2,5,8),
             (0,4,8),(2,4,6)]
    for i,j,k in lines:
        if b[i] != ' ' and b[i] == b[j] == b[k]:
            return b[i]
    return None

def is_draw(b):
    return winner(b) is None and all(c != ' ' for c in b)

def copy_board(b):
    return b[:]

# ----------------- Rollouts para evaluar una jugada -----------------

def random_policy_move(b, player):
    """Política simple para los rollouts: si hay jugada ganadora inmediata la toma,
    si puede bloquear pérdida inmediata bloquea; si no, juega al azar."""
    for i in available_moves(b):
        bb = copy_board(b)
        place(bb, i, player)
        if winner(bb) == player:
            return i
    opp = 'O' if player == 'X' else 'X'
    for i in available_moves(b):
        bb = copy_board(b)
        place(bb, i, opp)
        if winner(bb) == opp:
            return i
    return random.choice(available_moves(b))

def simulate_from_move(b, move, ai, hu):
    """Simula una partida completa desde la jugada 'move' del AI.
       Devuelve +1 si gana AI, 0 empate, -1 si pierde."""
    bb = copy_board(b)
    place(bb, move, ai)
    w = winner(bb)
    if w == ai: return 1
    if is_draw(bb): return 0

    turn = hu
    while True:
        m = random_policy_move(bb, turn)
        place(bb, m, turn)
        w = winner(bb)
        if w == ai: return 1
        if w == hu: return -1
        if is_draw(bb): return 0
        turn = ai if turn == hu else hu

def estimated_value(b, move, ai, hu, rollouts=40):
    """Promedia N simulaciones desde la jugada 'move'."""
    s = 0
    for _ in range(rollouts):
        s += simulate_from_move(b, move, ai, hu)
    return s / rollouts

# ----------------- Recocido Simulado para elegir jugada -----------------

def sa_choose_move(b, ai, hu, T0=5.0, Tf=0.1, alpha=0.95, L=20, rollouts=40):
    """Devuelve una casilla usando Simulated Annealing.
       - T0: temperatura inicial
       - Tf: temperatura final
       - alpha: factor de enfriamiento (geométrico)
       - L: iteraciones por temperatura
       - rollouts: simulaciones por evaluación"""
    empties = available_moves(b)
    # Si hay jugada ganadora inmediata o bloqueo, sé pragmático:
    for i in empties:
        bb = copy_board(b)
        place(bb, i, ai)
        if winner(bb) == ai:
            return i
    for i in empties:
        bb = copy_board(b)
        place(bb, i, hu)
        if winner(bb) == hu:
            return i

    # Candidato inicial: cualquiera libre
    current = random.choice(empties)
    best = current
    cur_val = estimated_value(b, current, ai, hu, rollouts=rollouts)
    best_val = cur_val

    T = T0
    while T > Tf and len(empties) > 1:
        for _ in range(L):
            # Vecino: otra casilla libre distinta
            neighbor = current
            while neighbor == current:
                neighbor = random.choice(empties)
            neigh_val = estimated_value(b, neighbor, ai, hu, rollouts=rollouts)
            dE = -(neigh_val - cur_val)  # energía = -valor
            # Aceptación de Metrópolis
            if dE < 0 or random.random() < math.exp(-dE / T):
                current, cur_val = neighbor, neigh_val
                if cur_val > best_val:
                    best, best_val = current, cur_val
        T *= alpha
    return best

# ----------------- Interfaz de juego -----------------

def ask_move(b, mark):
    while True:
        s = input(f"Turno de {mark}. Casillero (1-9): ").strip()
        try:
            i = int(s) - 1
            if i not in range(9): print("Rango 1-9, maestro."); continue
            if b[i] != ' ': print("Ocupado. Probá otro."); continue
            return i
        except:
            print("Número válido, por favor.")

def play_human_vs_sa(T0=5.0, Tf=0.1, alpha=0.95, L=20, rollouts=40):
    b = new_board()
    human = random.choice(['X', 'O'])
    ai = 'O' if human == 'X' else 'X'
    print(f"Vos sos {human}. La IA es {ai}.")
    print_board(b)
    turn = 'X'
    while True:
        if turn == human:
            i = ask_move(b, human)
            place(b, i, human)
        else:
            print(f"IA pensando con SA (T0={T0})...")
            i = sa_choose_move(b, ai, human, T0=T0, Tf=Tf, alpha=alpha, L=L, rollouts=rollouts)
            place(b, i, ai)
            print(f"IA juega en {i+1}.")
        print_board(b)
        w = winner(b)
        if w: print(f"Gana {w}."); return
        if is_draw(b): print("Empate."); return
        turn = 'O' if turn == 'X' else 'X'

def main():
    print("=== TA-TE-TI con Recocido Simulado ===")
    try:
        T0 = float(input("T0 (ej. 0.2, 1, 5, 10): ").strip() or "5")
    except:
        T0 = 0.8
    Tf = 0.1
    alpha = 0.95
    L = 20
    rollouts = 40
    play_human_vs_sa(T0=T0, Tf=Tf, alpha=alpha, L=L, rollouts=rollouts)

if __name__ == "__main__":
    main()
