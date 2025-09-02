def forward_chaining(reglas, hechos_iniciales, objetivo):
    """
    Implementa un motor de inferencia con encadenamiento hacia adelante.

    Args:
        reglas (list): Una lista de reglas en formato (premisa, conclusion).
                       Las premisas son un conjunto, y la conclusion es un string.
        hechos_iniciales (set): Un conjunto de hechos conocidos.
        objetivo (str): La proposición que se quiere demostrar.

    Returns:
        bool: True si el objetivo se puede derivar, False en caso contrario.
    """
    hechos_conocidos = set(hechos_iniciales)
    
    # Bucle que se ejecuta mientras se puedan derivar nuevos hechos.
    while True:
        nuevos_hechos_derivados = False
        
        # Iterar a través de cada regla en la base de conocimiento.
        for premisa, conclusion in reglas:
            # Comprobar si todas las proposiciones en la premisa son hechos conocidos.
            if premisa.issubset(hechos_conocidos):
                # Si la conclusión no es un hecho conocido, la añadimos.
                if conclusion not in hechos_conocidos:
                    hechos_conocidos.add(conclusion)
                    nuevos_hechos_derivados = True
                    print(f"Se ha inferido '{conclusion}' a partir de '{premisa}'")
        
        # Si no se ha derivado ningún nuevo hecho, el bucle se detiene.
        if not nuevos_hechos_derivados:
            break
            
    # Comprobar si el objetivo está en el conjunto de hechos conocidos.
    return objetivo in hechos_conocidos

# --- Prueba con las proposiciones del ejercicio 3 ---

# 1. Definir la base de conocimiento como reglas
# R1: b AND c -> a
# R2: d AND e -> b
# R3: g AND e -> b
# R4: e -> c
# R7: a AND g -> f
# Las premisas son conjuntos, para manejar AND.

reglas_ejercicio3 = [
    (frozenset(['b', 'c']), 'a'),
    (frozenset(['d', 'e']), 'b'),
    (frozenset(['g', 'e']), 'b'),
    (frozenset(['e']), 'c'),
    (frozenset(['a', 'g']), 'f')
]

# 2. Definir los hechos iniciales (del ejercicio 3)
# R5: d
# R6: e
# g no se menciona, por lo que no es un hecho.
hechos_ejercicio3 = {'d', 'e'}

# 3. Definir el objetivo
objetivo_a = 'a'

# 4. Ejecutar el motor de inferencia
print("Iniciando motor de inferencia con encadenamiento hacia adelante...")
resultado = forward_chaining(reglas_ejercicio3, hechos_ejercicio3, objetivo_a)

# 5. Imprimir el resultado
print("\n--- Resultado ---")
if resultado:
    print(f"Éxito: Se ha demostrado que '{objetivo_a}' es verdadero.")
else:
    print(f"Fallo: No se pudo demostrar que '{objetivo_a}' es verdadero.")