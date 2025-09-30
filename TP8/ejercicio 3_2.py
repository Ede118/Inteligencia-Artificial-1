import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

# --- Configuración y Generación de Datos ---
N_PUNTOS_TOTAL = 23
LIMITE_INFERIOR = 0
LIMITE_SUPERIOR = 5
N_PUNTOS_KMEANS = 20
N_CLUSTERS = 2
valores_k = [1, 3, 5] # Valores de K a probar

# Generar 23 puntos aleatorios en [0, 5]
puntos_totales = np.random.uniform(low=LIMITE_INFERIOR, high=LIMITE_SUPERIOR, size=(N_PUNTOS_TOTAL, 2))

# Preparar datos
puntos_entrenamiento = puntos_totales[:N_PUNTOS_KMEANS] # 20 puntos para K-means/K-NN entrenamiento
puntos_prueba_knn = puntos_totales[N_PUNTOS_KMEANS:]    # 3 puntos para K-NN prueba

# --- 3. Generación y Gráfico de 23 Puntos (Figura 1) ---
plt.figure(figsize=(8, 6))
plt.scatter(puntos_totales[:, 0], puntos_totales[:, 1], color='blue', label='23 Puntos Aleatorios')
plt.title('3. Puntos Aleatorios Generados en [0, 5]')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.xlim(LIMITE_INFERIOR - 0.5, LIMITE_SUPERIOR + 0.5)
plt.ylim(LIMITE_INFERIOR - 0.5, LIMITE_SUPERIOR + 0.5)
plt.grid(True)
plt.legend()


# ----------------------------------------------------------------------
# --- 3.1. Implementación de K-means (Entrenamiento) ---
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init='auto')
kmeans.fit(puntos_entrenamiento)
etiquetas_entrenamiento = kmeans.labels_ # Etiquetas (clase) de los 20 puntos
centroides = kmeans.cluster_centers_
cmap_colores = np.array(['green', 'orange']) # Color para Cluster 0 y Cluster 1

# ----------------------------------------------------------------------
# --- 3.2. Clasificación de los 3 puntos restantes con K-NN (Figura 2 con Subplots) ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
fig.suptitle('3.2. Clasificación K-NN de 3 Puntos Restantes con Distintos Valores de K', fontsize=16)

observaciones = []
marcadores_prueba = ['D', 's', '^'] # Diamante, Cuadrado, Triángulo para los 3 puntos

for i, k in enumerate(valores_k):
    # Seleccionar el subplot actual
    ax = axes[i]
    
    # 1. Entrenar K-NN para el valor de K actual
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(puntos_entrenamiento, etiquetas_entrenamiento)
    
    # 2. Predecir las etiquetas para los 3 puntos restantes
    etiquetas_predichas = knn.predict(puntos_prueba_knn)
    
    # 3. Almacenar observación
    observacion_str = f"K={k}: Etiquetas predichas: {etiquetas_predichas}"
    observaciones.append(observacion_str)
    
    # 4. Graficar los 20 puntos de entrenamiento (Fondo)
    ax.scatter(puntos_entrenamiento[:, 0], puntos_entrenamiento[:, 1], 
            c=cmap_colores[etiquetas_entrenamiento], s=80, 
            label='20 Puntos Clasificados (Entrenamiento)', alpha=0.6)
    
    # 5. Graficar Centroides
    ax.scatter(centroides[:, 0], centroides[:, 1], marker='X', s=150, color='black', label='Centroides K-means')
    
    # 6. Graficar los 3 Puntos de Prueba con el color predicho
    color_predicho = cmap_colores[etiquetas_predichas]
    for j in range(len(puntos_prueba_knn)):
        ax.scatter(puntos_prueba_knn[j, 0], puntos_prueba_knn[j, 1], 
                    marker=marcadores_prueba[j], s=180, 
                    color=color_predicho[j], edgecolors='red', linewidths=2,
                    label=f'Punto {j+1} Predicho ({cmap_colores[etiquetas_predichas[j]]})')
    
    # Configurar el subplot
    ax.set_title(f'Resultado con K = {k}')
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y' if i == 0 else '')
    ax.set_xlim(LIMITE_INFERIOR - 0.5, LIMITE_SUPERIOR + 0.5)
    ax.set_ylim(LIMITE_INFERIOR - 0.5, LIMITE_SUPERIOR + 0.5)
    ax.grid(True)
    ax.legend(loc='upper left', fontsize=8)


# --- Observaciones Anotadas (Sección de texto) ---
print("\n" + "=" * 50)
print("3.2. Clasificación K-NN: Resultados y Observaciones")
print("=" * 50)
print("El conjunto de entrenamiento son los 20 puntos previamente clasificados por K-means (Verde/Naranja).")
print("Los 3 puntos de prueba son clasificados según el voto de sus K vecinos más cercanos.")
print("-" * 50)
for obs in observaciones:
    print(obs)
print("-" * 50)

# Mostrar ambas figuras simultáneamente
plt.show()