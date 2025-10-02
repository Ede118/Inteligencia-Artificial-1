import numpy as np
import random

# Configuración
gamma = 0.9         # factor despreciativo (descuento)
alpha = 0.8         # tasa de aprendizaje
episodes = 8000     # nº de episodios de entrenamiento
epsilon_ini = 0.2   # exploración inicial (epsilon-greedy)
epsilon_fin = 0.01  # exploración mínima
seed = 0            # para reproducibilidad (opcional)

random.seed(seed)
np.random.seed(seed)

# -----------------------------
# Matriz de recompensas R 
# -1: transición no permitida
#  0: transición neutra
# 100: transición a objetivo
# -----------------------------
R = np.array([
    [-1,  0,  0, -1, -1, -1],
    [ 0, -1, -1,  0, -1, -1],
    [ 0, -1, -1, -1,  0, -1],
    [-1,  0, -1, -1,  0, 100],
    [-1, -1,  0,  0, -1, 100],
    [-1, -1, -1,  0,  0, 100],
], dtype=float)

n_states = R.shape[0]
goal_state = 5  # estado objetivo 

# Acciones válidas desde cada estado
valid_actions = {s: np.where(R[s] != -1)[0] for s in range(n_states)}

# -----------------------------
# Entrenamiento Q-learning
# -----------------------------
Q = np.zeros_like(R, dtype=float)

def choose_action(state, epsilon):
    actions = valid_actions[state]
    if random.random() < epsilon:
        return int(random.choice(actions))  # explorar
    # explotar: mejor acción por valor Q
    qvals = Q[state, actions]
    return int(actions[np.argmax(qvals)])

def next_state_from_action(action):
    # En este entorno, la acción es el siguiente estado (grafo dirigido)
    return action

for ep in range(episodes):
    # epsilon que decae linealmente
    epsilon = max(epsilon_fin, epsilon_ini * (1 - ep / episodes))

    # arranca en un estado aleatorio (puede ser objetivo; si lo es, reinicia)
    s = np.random.randint(0, n_states)
    if s == goal_state:
        s = np.random.randint(0, n_states)

    # episodio hasta alcanzar objetivo
    while True:
        a = choose_action(s, epsilon)
        s_next = next_state_from_action(a)

        # recompensa inmediata
        r = R[s, a]

        # valor futuro máximo desde s_next, pero sólo sobre acciones válidas
        if len(valid_actions[s_next]) > 0:
            max_next = np.max(Q[s_next, valid_actions[s_next]])
        else:
            max_next = 0.0

        # actualización Q-learning
        Q[s, a] = (1 - alpha) * Q[s, a] + alpha * (r + gamma * max_next)

        s = s_next
        if s == goal_state:  # término del episodio
            break

# -----------------------------
# Resultados
# -----------------------------
# Matriz Q aprendida
print("Q (valores crudos):\n", np.round(Q, 2))

# Normalización respecto al valor máximo encontrado en Q
Q_max = np.max(Q)
if Q_max > 0:
    Q_norm = (Q / Q_max) 
else:
    Q_norm = Q.copy()

print("\nQ normalizada respecto al máximo valor encontrado:\n", np.round(Q_norm, 3))

# Política óptima (mejor acción por estado, restringida a acciones válidas)
policy = {}
for s in range(n_states):
    acts = valid_actions[s]
    if len(acts) == 0:
        policy[s] = None
        continue
    best_a = acts[np.argmax(Q[s, acts])]
    policy[s] = int(best_a)

print("\nPolítica óptima (mejor acción por estado):")
for s in range(n_states):
    if policy[s] is None:
        print(f"  Estado {s}: (sin acciones)")
    else:
        print(f"  Estado {s} -> ir a {policy[s]}")

# trayectoria codiciosa desde cada estado hasta el objetivo
def greedy_path(start):
    s = start
    path = [s]
    visited = set()
    while s != goal_state and s not in visited and len(valid_actions[s]) > 0:
        visited.add(s)
        s = policy[s]
        path.append(s)
    return path

print("\nTrayectorias codiciosas (con la política aprendida):")
for s in range(n_states):
    if s == goal_state:
        continue
    print(f"  {s}: {greedy_path(s)}")
