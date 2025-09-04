import os

def forward_chaining(SetReglas, SetVerdades, Objetive, verbose=True):
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

    if SetReglas is None or SetVerdades is None or Objetive is None:
        raise ValueError("SetReglas, SetVerdades y Objetive no pueden ser None.")
    elif not isinstance(SetReglas, list) or not all(isinstance(r, tuple) and len(r) == 2 and isinstance(r[0], frozenset) and isinstance(r[1], str) for r in SetReglas):
        raise ValueError("SetReglas debe ser una lista de tuplas (premisa, conclusion) donde la premisa es un frozenset y la conclusion es un string.")
    elif not isinstance(SetVerdades, set) or not all(isinstance(h, str) for h in SetVerdades):
        raise ValueError("SetVerdades debe ser un conjunto de strings.")
    elif not isinstance(Objetive, str):
        raise ValueError("Objetive debe ser un string.")
    

    # Por si el objetivo ya es un hecho
    if Objetive in SetVerdades:
        if verbose: print(f"Objetivo '{Objetive}' ya estaba en los hechos.")
        return True
    
    nombre_por_premisa = {
        frozenset({'b','c'}): 'R1',
        frozenset({'d','e'}): 'R2',
        frozenset({'g','e'}): 'R3',
        frozenset({'e'}):     'R4',
        frozenset({'a','g'}): 'R7',
    }
    
    nuevos_hechos_derivados = True

    # Bucle que se ejecuta mientras se puedan derivar nuevos hechos.
    while nuevos_hechos_derivados:

        # Cuando se completa el ciclo sin derivar nuevos hechos, se detiene.
        nuevos_hechos_derivados = False
        
        # Iterar a través de cada regla en la base de conocimiento.
        for premisa, conclusion in SetReglas:

            # Comprobar si todas las proposiciones en la premisa son hechos conocidos.
            # Si la conclusión no es un hecho conocido, la añadimos.
            
            if premisa.issubset(SetVerdades) and conclusion not in SetVerdades:
                    
                    SetVerdades.add(conclusion)
                    nuevos_hechos_derivados = True 

                    regla = nombre_por_premisa.get(premisa, '?')

                    prem_str = ' ∧ '.join(sorted(premisa))
                    
                    print(f" >>Se ha inferido '{conclusion}' a partir de '{regla}'")
                    print(f"{regla}: {prem_str} ⟹ {conclusion}\n")

                    if conclusion == Objetive:
                        if verbose: print(f"Objetivo '{Objetive}' alcanzado.")
                        nuevos_hechos_derivados = False
                        return True
            
    # Comprobar si el objetivo está en el conjunto de hechos conocidos.
    return Objetive in SetVerdades

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



if __name__ == "__main__":

    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

    # 4. Ejecutar el motor de inferencia
    print("--- Base de Conocimiento ---")

    for s in ["R1: b ∧ c → a",
          "R2: d ∧ e → b",
          "R3: g ∧ e → b",
          "R4: e → c",
          "R5: d",
          "R6: e",
          "R7: a ∧ g → f"]:
        print(s)

    print("\nIniciando motor de inferencia con encadenamiento hacia adelante...\n")
    resultado = forward_chaining(reglas_ejercicio3, hechos_ejercicio3, objetivo_a)

    # 5. Imprimir el resultado
    print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("| \t\t\t Resultado \t\t\t      |")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if resultado:
        print(f"\n >>Éxito: Se ha demostrado que '{objetivo_a}' es verdadero.")
    else:
        print(f"\n >>Fallo: No se pudo demostrar que '{objetivo_a}' es verdadero.")