# Definición de adyacencias (grafo de las piezas)
adj = {
    1:{2},
    2:{1,3,6},
    3:{2,4,5,6},
    4:{5,12},
    5:{3,4,6,10,12,13,14},
    6:{3,5,7,8},
    7:{6,7,9,10},
    8:{6,9},
    9:{7,8,10,11},
    10:{5,7,9,11,14,15,16},
    11:{9,10,16,17},
    12:{4,5,13},
    13:{5,12,14},
    14:{10,13,15},
    15:{14,16},
    16:{11,15,17},
    17:{11,16},
}

# Colores disponibles
colors = ["R","N","Am","Ve","Az","Vi","M"]

# Inicializar dominios
domains = {v:set(colors) for v in adj}
assignment = {}

def choose_value_most_constraining(var):
    """
    Selecciona el valor más restringido (VMR):
    el que elimina más posibilidades en los vecinos,
    respetando el orden definido en 'colors'.
    """
    best_val = None
    best_score = None
    for val in colors:  # respeta el orden original
        if val not in domains[var]:
            continue
        score = 0
        for nb in adj[var]:
            if nb in assignment:
                continue
            if val in domains[nb]:
                score += 1
        if best_score is None or score > best_score:
            best_val = val
            best_score = score
    return best_val

def forward_checking():
    """Asigna colores paso a paso usando Forward Checking + VMR"""
    for var in range(1,18):  # piezas del 1 al 17
        val = choose_value_most_constraining(var)
        if not val:
            print(f"¡Fallo! No hay valor posible para la variable {var}")
            return None
        # Asignar
        assignment[var] = val
        print(f"Pieza {var} -> {val}")
        # Podar en vecinos
        for nb in adj[var]:
            if nb not in assignment and val in domains[nb]:
                domains[nb].remove(val)

    return assignment

# Ejecutar
solution = forward_checking()

print("\n--- Asignación final de colores ---")
for var in sorted(solution.keys()):
    print(f"Pieza {var}: {solution[var]}")
