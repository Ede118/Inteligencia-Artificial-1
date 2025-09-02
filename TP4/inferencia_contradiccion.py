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

def motor_inconsistencia_resolucion(clausulas):
    """
    Motor de inferencia que detecta inconsistencias usando resolución.

    Args:
        clausulas (list): Una lista de conjuntos inmutables (frozenset) de literales.

    Returns:
        bool: True si el conjunto es inconsistente, False en caso contrario.
    """
    clausulas_conocidas = set(clausulas)
    
    while True:
        nuevas_clausulas = set()
        pares_clausulas = itertools.combinations(clausulas_conocidas, 2)
        
        for c1, c2 in pares_clausulas:
            resultado_resolucion = resolver_clausulas(c1, c2)
            
            if resultado_resolucion is not None:
                print(f"Resolviendo {c1} y {c2} -> {resultado_resolucion}")
                
                if not resultado_resolucion:  # La cláusula vacía {}
                    print("\n¡Inconsistencia detectada! Se ha derivado la cláusula vacía.")
                    return True
                
                # Si la nueva cláusula no es trivial y no se ha visto antes.
                if resultado_resolucion not in clausulas_conocidas:
                    nuevas_clausulas.add(resultado_resolucion)
        
        # Si no se generan nuevas cláusulas, no hay contradicción.
        if not nuevas_clausulas:
            print("\nNo se encontraron nuevas cláusulas. El conjunto de proposiciones es consistente.")
            return False
            
        clausulas_conocidas.update(nuevas_clausulas)

# --- Prueba con un conjunto inconsistente ---
# Para probar la inconsistencia, añadiremos una regla que contradice
# las premisas. Por ejemplo, sabemos que 'c' es True, así que si agregamos
# la negación de 'c', causaremos una contradicción.

# Base de conocimiento del ejercicio 3 convertida a FNC:
# R1: b AND c -> a  --> ¬b v ¬c v a
# R2: d AND e -> b  --> ¬d v ¬e v b
# R3: g AND e -> b  --> ¬g v ¬e v b
# R4: e -> c      --> ¬e v c
# R5: d           --> d
# R6: e           --> e

# Convertimos las proposiciones a un formato de conjunto.
clausulas_base = [
    frozenset(['¬b', '¬c', 'a']),
    frozenset(['¬d', '¬e', 'b']),
    frozenset(['¬g', '¬e', 'b']),
    frozenset(['¬e', 'c']),
    frozenset(['d']),
    frozenset(['e'])
]

# Añadimos una proposición que haga el conjunto inconsistente.
# Sabemos que de 'e' (R6) y '¬e v c' (R4) se deriva 'c'.
# Por lo tanto, si añadimos '¬c', el conjunto será inconsistente.
clausulas_inconsistentes = clausulas_base + [frozenset(['¬c'])]

# Ejecutar el motor
print("Analizando la base de conocimiento para detectar inconsistencia...")
es_inconsistente = motor_inconsistencia_resolucion(clausulas_inconsistentes)

print("\n--- Resultado ---")
if es_inconsistente:
    print("El conjunto de proposiciones es inconsistente. ¡Prueba exitosa! ✅")
else:
    print("El conjunto de proposiciones es consistente.")