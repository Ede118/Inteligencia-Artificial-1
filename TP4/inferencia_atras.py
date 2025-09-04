import os

def backward_chaining(SetReglas, SetVerdades, Objetive):
    """
    Implementa un motor de inferencia con encadenamiento hacia atrás.

    Args:
        SetReglas (list): Una lista de reglas en formato (premisa, conclusion).
                       Las premisas son un conjunto, y la conclusion es un string.
        SetVerdades (set): Un conjunto de hechos conocidos.
        Objetive (str): La proposición que se quiere demostrar.

    Returns:
        bool: True si el objetivo se puede derivar, False en caso contrario.
    """

    if SetReglas is None or SetVerdades is None or Objetive is None:
        raise ValueError("SetReglas, SetVerdades y Objetive no pueden ser None.")
    elif not isinstance(SetReglas, list) or not all(isinstance(r, tuple) and len(r) == 2 and isinstance(r[0], frozenset) and isinstance(r[1], str) for r in SetReglas):
        raise ValueError("SetReglas debe ser una lista de tuplas (premisa, conclusion) donde la premisa es un frozenset y la conclusion es un string.")
    elif not isinstance(SetVerdades, set) or not all(isinstance(h, str) for h in SetVerdades):
        raise ValueError("SetVerdades debe ser un conjunto de strings.")
    elif not isinstance(Objetive, str):
        raise ValueError("Objetive debe ser un string.")
    
    
    # 1. Caso base: El objetivo ya es un hecho conocido.
    if Objetive in SetVerdades:
        print(f"\n >>Éxito: El objetivo '{Objetive}' ya es un hecho conocido.")
        return True
    

    nombre_por_premisa = {
        frozenset({'b','c'}): 'R1',
        frozenset({'d','e'}): 'R2',
        frozenset({'g','e'}): 'R3',
        frozenset({'e'}):     'R4',
        frozenset({'a','g'}): 'R7',
    }
    
    # 2. Búsqueda de reglas que pueden probar el objetivo.
    RulesAvaible = [regla for regla in SetReglas if regla[1] == Objetive]

    # 3. Si no hay reglas para probar el objetivo, la prueba falla.
    if not RulesAvaible:
        print("\n-----------------------------------------------------------")
        print(f"Fallo: No hay reglas para probar el objetivo '{Objetive}'.")
        print("-----------------------------------------------------------\n")
        return False
        
    # 4. Intentar probar el objetivo a través de cada regla posible.
    for premisa, _ in RulesAvaible:

        RuleName = nombre_por_premisa.get(premisa, '?')

        print(f"\nIntentando probar '{Objetive}' usando la regla '{RuleName}'")
        print(f"{RuleName}: {' ∧ '.join(sorted(premisa))} → {Objetive}")
        
        flag_subobjetivos = True
        
        # 5. Intentar probar cada subobjetivo en la premisa.
        for sub_objetivo in premisa:
            # Llamada recursiva para probar el subobjetivo.
            if not backward_chaining(SetReglas, SetVerdades, sub_objetivo):
                flag_subobjetivos = False
                break

        # 6. Si todos los subobjetivos se probaron, el objetivo es verdadero.
        if flag_subobjetivos:
            print(f"\n >>Éxito: Se ha demostrado que '{Objetive}' es verdadero usando la regla '{RuleName}'.")
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

if __name__ == "__main__":

    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()


    # 4. Imprimir la base de conocimiento
    print("--- Base de Conocimiento ---")
    for s in ["R1: b ∧ c → a",
          "R2: d ∧ e → b",
          "R3: g ∧ e → b",
          "R4: e → c",
          "R5: d",
          "R6: e",
          "R7: a ∧ g → f"]:
        print(s)

    # 5. Ejecutar el motor de inferencia
    print("\nIniciando motor de inferencia con encadenamiento hacia atrás...\n")
    resultado = backward_chaining(reglas_ejercicio3, hechos_ejercicio3, objetivo_a)

    # 5. Imprimir el resultado
    print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("| \t\t\t Resultado \t\t\t      |")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if resultado:
        print(f"\n >>Éxito: Se ha demostrado que '{objetivo_a}' es verdadero.")
    else:
        print(f"\n >>Fallo: No se pudo demostrar que '{objetivo_a}' es verdadero.")