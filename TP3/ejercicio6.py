import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

# --- Datos del Problema ---
#             Caja: 1    2    3    4    5    6    7    8    9    10
precios = np.array([100, 50, 115, 25, 200, 30, 40, 100, 100, 100])
pesos   = np.array([300, 200, 450, 145, 664, 90, 150, 355, 401, 395])
capacidad_maxima = 1000
n_cajas = 10

# --- Parámetros del Algoritmo Genético ---
tamano_poblacion = 50       # Un número par, como se recomienda (N)
tasa_mutacion = 0.05        # Probabilidad de que un gen (caja) mute
num_generaciones = 200      # Mecanismo de detención

# --- 6.2 Generación de la Población Inicial ---
def crear_poblacion_inicial(tamano, n_items, pesos_items, capacidad):
    poblacion = []
    while len(poblacion) < tamano:
        individuo = np.random.randint(2, size=n_items)
        peso_actual = np.sum(individuo * pesos_items)
        if peso_actual <= capacidad:
            poblacion.append(individuo)
    return np.array(poblacion)

# --- 6.3 Función de Idoneidad y Selección por Ruleta ---
def calcular_idoneidad(poblacion, precios_items):
    return np.dot(poblacion, precios_items)

def seleccion_ruleta(poblacion, idoneidad):
    suma_idoneidad = np.sum(idoneidad)
    if suma_idoneidad == 0:
        probabilidades = np.ones(len(poblacion)) / len(poblacion)
    else:
        probabilidades = idoneidad / suma_idoneidad
    indices_elegidos = np.random.choice(len(poblacion), size=len(poblacion), p=probabilidades)
    return poblacion[indices_elegidos]

# --- 6.4 Cruce, Mutación y Verificación ---
def cruce_y_mutacion(padres, pesos_items, capacidad, tasa_mut):
    nueva_generacion = []
    np.random.shuffle(padres)
    for i in range(0, len(padres), 2):
        padre1 = padres[i]
        padre2 = padres[i+1] if i + 1 < len(padres) else padres[i]
        
        punto_cruce = np.random.randint(1, len(padre1))
        hijo1 = np.concatenate([padre1[:punto_cruce], padre2[punto_cruce:]])
        hijo2 = np.concatenate([padre2[:punto_cruce], padre1[punto_cruce:]])
        
        for j in range(len(hijo1)):
            if np.random.rand() < tasa_mut:
                hijo1[j] = 1 - hijo1[j]
            if np.random.rand() < tasa_mut:
                hijo2[j] = 1 - hijo2[j]

        if np.sum(hijo1 * pesos_items) <= capacidad:
            nueva_generacion.append(hijo1)
        else:
            nueva_generacion.append(padre1)
        if np.sum(hijo2 * pesos_items) <= capacidad:
            nueva_generacion.append(hijo2)
        else:
            nueva_generacion.append(padre2)
            
    return np.array(nueva_generacion)

# --- 6.5 Proceso Iterativo y Resultado Final ---

print("--- Iniciando Evolución del Algoritmo Genético ---\n")

mejor_individuo_global = None
mejor_idoneidad_global = -1

poblacion = crear_poblacion_inicial(tamano_poblacion, n_cajas, pesos, capacidad_maxima)

for generacion in range(num_generaciones):
    idoneidad = calcular_idoneidad(poblacion, precios)
    
    # Encontrar el mejor individuo de la generación actual
    indice_mejor_gen = np.argmax(idoneidad)
    mejor_individuo_gen = poblacion[indice_mejor_gen]
    mejor_idoneidad_gen = idoneidad[indice_mejor_gen]
    
    # Actualizar el mejor individuo global si es necesario
    if mejor_idoneidad_gen > mejor_idoneidad_global:
        mejor_idoneidad_global = mejor_idoneidad_gen
        mejor_individuo_global = mejor_individuo_gen

    # *** NUEVA LÍNEA PARA MOSTRAR EL PROGRESO ***
    # Muestra el mejor resultado encontrado HASTA AHORA en cada generación
    peso_actual = np.sum(mejor_individuo_global * pesos)
    print(f"Generación {generacion+1:03d} | Mejor Precio: ${mejor_idoneidad_global:<4} | Peso: {peso_actual:<4} kg | Solución: {mejor_individuo_global}")

    padres = seleccion_ruleta(poblacion, idoneidad)
    poblacion = cruce_y_mutacion(padres, pesos, capacidad_maxima, tasa_mutacion)

# --- Mostrar Resultados Finales ---
precio_final = np.sum(mejor_individuo_global * precios)
peso_final = np.sum(mejor_individuo_global * pesos)
cajas_seleccionadas = np.where(mejor_individuo_global == 1)[0] + 1

print("\n--- Mejor Solución Encontrada ---")
print(f"📦 Cajas a cargar: {list(cajas_seleccionadas)}")
print(f"⚖️ Peso Total: {peso_final} kg (Límite: {capacidad_maxima} kg)")
print(f"💲 Precio Total: ${precio_final}")
print(f"🧬 Individuo (genotipo): {mejor_individuo_global}")