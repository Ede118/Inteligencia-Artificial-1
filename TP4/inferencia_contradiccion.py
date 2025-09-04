import itertools

def to_cnf(regla):
    """
    Convierte una regla simple (implicación) a FNC.
    Asume que la premisa es una conjunción de literales.
    """
    premisa, conclusion = regla
    literales_premisa = [f"¬{p}" for p in premisa]
    
    # La implicación (A -> B) se convierte en ¬A v B
    # donde A es la conjunción de la premisa.
    return frozenset(literales_premisa + [conclusion])

def resolver_clausulas(c1, c2):
    """
    Aplica la regla de resolución a dos cláusulas.
    Retorna la cláusula resuelta o None si no se pueden resolver.
    """
    for literal in c1:
        negado = f"¬{literal}" if not literal.startswith("¬") else literal[1:]
        if negado in c2:
            nueva_clausula = (c1 - {literal}) | (c2 - {negado})
            return nueva_clausula
    return None

def formato_clausula(clausula):
    """
    Función auxiliar para formatear una cláusula para una salida legible.
    Convierte un frozenset a una cadena de texto.
    """
    if not clausula:
        return "□ (Cláusula Vacía)"
    return " v ".join(sorted(list(clausula)))

def motor_inconsistencia_resolucion(clausulas):
    """
    Motor de inferencia que detecta inconsistencias usando resolución.

    Args:
        clausulas (list): Una lista de conjuntos inmutables (frozenset) de literales.

    Returns:
        bool: True si el conjunto es inconsistente, False en caso contrario.
    """
    clausulas_conocidas = set(clausulas)
    
    print("Analizando la base de conocimiento para detectar inconsistencia...")
    
    # --- Nuevo: Imprimir la base de conocimiento inicial ---
    print("\nBase de conocimiento inicial:")
    for i, c in enumerate(clausulas):
        print(f"  Cláusula {i+1}: ({formato_clausula(c)})")
    print("-" * 30)

    while True:
        nuevas_clausulas = set()
        pares_clausulas = itertools.combinations(clausulas_conocidas, 2)
        
        for c1, c2 in pares_clausulas:
            resultado_resolucion = resolver_clausulas(c1, c2)
            
            if resultado_resolucion is not None:
                print(f"Resolviendo ({formato_clausula(c1)}) y ({formato_clausula(c2)}) -> ({formato_clausula(resultado_resolucion)})")
                
                if not resultado_resolucion: 
                    print("\n¡Inconsistencia detectada! Se ha derivado la cláusula vacía.")
                    return True
                
                if resultado_resolucion not in clausulas_conocidas:
                    nuevas_clausulas.add(resultado_resolucion)
        
        if not nuevas_clausulas:
            print("\nNo se encontraron nuevas cláusulas. El conjunto de proposiciones es consistente.")
            return False
            
        clausulas_conocidas.update(nuevas_clausulas)

# --- Prueba con un conjunto inconsistente ---
clausulas_base = [
    frozenset(['¬b', '¬c', 'a']),
    frozenset(['¬d', '¬e', 'b']),
    frozenset(['¬g', '¬e', 'b']),
    frozenset(['¬e', 'c']),
    frozenset(['d']),
    frozenset(['e'])
]

# Añadimos la proposición que hace que el conjunto sea inconsistente.
clausulas_inconsistentes = clausulas_base + [frozenset(['¬c'])]

if __name__ == "__main__":
    print("--- Resultado ---")
    es_inconsistente = motor_inconsistencia_resolucion(clausulas_inconsistentes)
    if es_inconsistente:
        print("\nEl conjunto de proposiciones es inconsistente. ¡Prueba exitosa! ✅")
    else:
        print("\nEl conjunto de proposiciones es consistente.")