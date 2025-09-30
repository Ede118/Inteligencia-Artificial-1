import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# --- 3. Generar un conjunto de 23 puntos ---
N_PUNTOS_TOTAL = 23
LIMITE_INFERIOR = 0
LIMITE_SUPERIOR = 5
N_PUNTOS_KMEANS = 20
N_CLUSTERS = 2

# Generar 23 puntos con coordenadas (x, y) aleatorias en [0, 5]
puntos_totales = np.random.uniform(low=LIMITE_INFERIOR, high=LIMITE_SUPERIOR, size=(N_PUNTOS_TOTAL, 2))

# Preparar datos para K-means
puntos_kmeans = puntos_totales[:N_PUNTOS_KMEANS]
puntos_excluidos = puntos_totales[N_PUNTOS_KMEANS:]

# --- Gráfico 1: Los 23 puntos iniciales ---
# Crea la PRIMERA figura
plt.figure(figsize=(8, 6))
plt.scatter(puntos_totales[:, 0], puntos_totales[:, 1], color='blue', label='23 Puntos Aleatorios')
plt.title('3. Puntos Aleatorios Generados en [0, 5]')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.xlim(LIMITE_INFERIOR - 0.5, LIMITE_SUPERIOR + 0.5)
plt.ylim(LIMITE_INFERIOR - 0.5, LIMITE_SUPERIOR + 0.5)
plt.grid(True)
plt.legend()


# --- 3.1 Implementar un algoritmo K-means ---
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init='auto')
kmeans.fit(puntos_kmeans)
etiquetas = kmeans.labels_
centroides = kmeans.cluster_centers_

# --- Gráfico 2: Resultado de K-means ---
# Crea la SEGUNDA figura
plt.figure(figsize=(8, 6))

# Graficar los 20 puntos clasificados
plt.scatter(puntos_kmeans[:, 0], puntos_kmeans[:, 1], c=etiquetas, cmap='cool', s=100, label=f'{N_PUNTOS_KMEANS} Puntos Clasificados (K-means)')

# Graficar los centroides
plt.scatter(centroides[:, 0], centroides[:, 1], marker='X', s=200, color='black', label='Centroides', linewidths=2)

# Graficar los puntos excluidos
plt.scatter(puntos_excluidos[:, 0], puntos_excluidos[:, 1], marker='o', s=50, color='gray', alpha=0.5, label='3 Puntos Excluidos')

plt.title(f'3.1. Clasificación K-means de {N_PUNTOS_KMEANS} Puntos en {N_CLUSTERS} Grupos')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.xlim(LIMITE_INFERIOR - 0.5, LIMITE_SUPERIOR + 0.5)
plt.ylim(LIMITE_INFERIOR - 0.5, LIMITE_SUPERIOR + 0.5)
plt.grid(True)
plt.legend()

# --- Llamada UNICA a plt.show() al final ---
# Esta única llamada mostrará AMBAS figuras creadas anteriormente.
plt.show()