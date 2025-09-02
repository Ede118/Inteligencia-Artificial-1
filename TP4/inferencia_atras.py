def backward_chaining(reglas, hechos_iniciales, objetivo):
    """
    Implementa un motor de inferencia con encadenamiento hacia atrás.

    Args:
        reglas (list): Una lista de reglas en formato (premisa, conclusion).
                       Las premisas son un conjunto, y la conclusion es un string.
        hechos_iniciales (set): Un conjunto de hechos conocidos.
        objetivo (str): La proposición que se quiere demostrar.

    Returns:
        bool: True si el objetivo se puede derivar, False en caso contrario.
    """
    # 1. Caso base: El objetivo ya es un hecho conocido.
    if objetivo in hechos_iniciales:
        print(f"Éxito: El objetivo '{objetivo}' ya es un hecho conocido.")
        return True
    
    # 2. Búsqueda de reglas que pueden probar el objetivo.
    reglas_posibles = [regla for regla in reglas if regla[1] == objetivo]

    # 3. Si no hay reglas para probar el objetivo, la prueba falla.
    if not reglas_posibles:
        print(f"Fallo: No hay reglas para probar el objetivo '{objetivo}'.")
        return False
        
    # 4. Intentar probar el objetivo a través de cada regla posible.
    for premisa, _ in reglas_posibles:
        print(f"Intentando probar '{objetivo}' usando la regla con premisa '{premisa}'")
        
        todos_subobjetivos_probados = True
        
        # 5. Intentar probar cada subobjetivo en la premisa.
        for sub_objetivo in premisa:
            # Llamada recursiva para probar el subobjetivo.
            if not backward_chaining(reglas, hechos_iniciales, sub_objetivo):
                todos_subobjetivos_probados = False
                break
        
        # 6. Si todos los subobjetivos se probaron, el objetivo es verdadero.
        if todos_subobjetivos_probados:
            print(f"Éxito: Todos los subobjetivos para '{objetivo}' fueron probados. Conclusión alcanzada.")
            return True
            
    # 7. Si ninguna regla pudo probar el objetivo, la prueba falla.
    return False

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
hechos_ejercicio3 = {'d', 'e'}

# 3. Definir el objetivo
objetivo_a = 'a'

# 4. Ejecutar el motor de inferencia
print("Iniciando motor de inferencia con encadenamiento hacia atrás...")
resultado = backward_chaining(reglas_ejercicio3, hechos_ejercicio3, objetivo_a)

# 5. Imprimir el resultado
print("\n--- Resultado ---")
if resultado:
    print(f"Éxito: Se ha demostrado que '{objetivo_a}' es verdadero.")
else:
    print(f"Fallo: No se pudo demostrar que '{objetivo_a}' es verdadero.")