import random
import sys

# Para que la consola no falle con caracteres especiales
sys.stdout.reconfigure(encoding='utf-8')

# Datos de las cajas: (peso, precio)
cajas = [
    (300, 100),  # Caja 1
    (200, 50),   # Caja 2
    (450, 115),  # Caja 3
    (145, 25),   # Caja 4
    (664, 200),  # Caja 5
    (90, 30),    # Caja 6
    (150, 40),   # Caja 7
    (355, 100),  # Caja 8
    (401, 100),  # Caja 9
    (395, 100)   # Caja 10
]

PESO_MAX = 1000
TAM_POBLACION = 50
GENERACIONES = 200
PROB_MUTACION = 0.1

# Evaluar fitness de una solución (vector binario de 10 posiciones)
def fitness(individuo):
    peso_total = sum(cajas[i][0] for i in range(len(cajas)) if individuo[i] == 1)
    valor_total = sum(cajas[i][1] for i in range(len(cajas)) if individuo[i] == 1)
    if peso_total > PESO_MAX:
        return 0  # inválido
    return valor_total

# Crear individuo aleatorio (10 bits)
def crear_individuo():
    return [random.randint(0, 1) for _ in range(len(cajas))]

# Selección por ruleta
def seleccionar(poblacion):
    fitness_vals = [fitness(ind) for ind in poblacion]
    total_fitness = sum(fitness_vals)

    if total_fitness == 0:
        return random.choice(poblacion)

    pick = random.uniform(0, total_fitness)
    acumulado = 0
    for ind, fit in zip(poblacion, fitness_vals):
        acumulado += fit
        if acumulado >= pick:
            return ind

# Cruce de un punto
def cruzar(p1, p2):
    punto = random.randint(1, len(cajas) - 1)
    return p1[:punto] + p2[punto:]

# Mutación (flip de un bit)
def mutar(individuo):
    if random.random() < PROB_MUTACION:
        idx = random.randint(0, len(cajas) - 1)
        individuo[idx] = 1 - individuo[idx]
    return individuo

# Algoritmo genético
def algoritmo_genetico():
    poblacion = [crear_individuo() for _ in range(TAM_POBLACION)]
    
    for g in range(GENERACIONES):
        nueva_poblacion = []
        for _ in range(TAM_POBLACION):
            padre1 = seleccionar(poblacion)
            padre2 = seleccionar(poblacion)
            hijo = cruzar(padre1, padre2)
            hijo = mutar(hijo)
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion
        mejor = max(poblacion, key=fitness)
        peso_mejor = sum(cajas[i][0] for i in range(len(cajas)) if mejor[i] == 1)
        print(f"Gen {g+1}: Mejor valor = {fitness(mejor)}, Peso = {peso_mejor}")

    return max(poblacion, key=fitness)

# Ejecutar
mejor_sol = algoritmo_genetico()
peso_final = sum(cajas[i][0] for i in range(len(cajas)) if mejor_sol[i] == 1)
valor_final = fitness(mejor_sol)

# Mostrar resultado
cajas_seleccionadas = [i+1 for i in range(len(cajas)) if mejor_sol[i] == 1]

print("\n📦 Mejor Solución Encontrada ---")
print("Cajas a cargar:", cajas_seleccionadas)
print("Peso total:", peso_final, "kg")
print("Valor total:", valor_final, "$")
