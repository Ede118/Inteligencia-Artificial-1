# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt

# ---------------------------
# Parámetros del problema
# ---------------------------
N = 1000  # tornillos por caja
OBS = "C"  # recubrimiento observado en TODAS las extracciones (N, C, o Z)

# Priors P(A..E) como vector columna
p = [0.15, 0.15, 0.50, 0.10, 0.10]  # [A, B, C, D, E]

# Mezclas por hipótesis
mix = {
    "A": {"N": 1.00, "C": 0.00, "Z": 0.00},
    "B": {"N": 0.70, "C": 0.20, "Z": 0.10},
    "C": {"N": 0.50, "C": 0.25, "Z": 0.25},
    "D": {"N": 0.20, "C": 0.50, "Z": 0.30},
    "E": {"N": 0.00, "C": 1.00, "Z": 0.00},
}

Ks = [
    int(round(N * mix["A"][OBS])),
    int(round(N * mix["B"][OBS])),
    int(round(N * mix["C"][OBS])),
    int(round(N * mix["D"][OBS])),
    int(round(N * mix["E"][OBS])),
]  # [K_A, K_B, K_C, K_D, K_E]

T_MAX = 10
T = list(range(0, T_MAX + 1))

def falling_ratio(K, N, t):
    if t == 0:
        return 1.0
    if K < t:
        return 0.0
    num = 1.0
    den = 1.0
    for j in range(t):
        num *= (K - j)
        den *= (N - j)
        if num == 0.0:
            return 0.0
    return num / den

V = []
U = []
alpha = []

for t in T:
    v_t = [falling_ratio(Ks[i], N, t) for i in range(5)]
    V.append(v_t)
    a_t = sum(p[i] * v_t[i] for i in range(5))
    alpha.append(a_t)
    if a_t == 0.0:
        U.append([1.0/5]*5)
    else:
        U.append([(p[i] * v_t[i]) / a_t for i in range(5)])

labels = ["A:100% N", "B:70N-20C-10Z", "C:50N-25C-25Z", "D:20N-50C-30Z", "E:100% C"]

# 1) Verosimilitud (semilog)
plt.figure()
for i in range(5):
    ys = [max(1e-300, V[t][i]) for t in T]
    plt.semilogy(T, ys, label=labels[i])
plt.xlim(0, T_MAX)
plt.xticks(T)
plt.xlabel("Número de tornillos extraídos (t)")
plt.ylabel(f"Verosimilitud acumulada v_t para OBS = {OBS}")
plt.title("Verosimilitud (hipergeométrica, sin reemplazo)")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("./Imagenes/verosimilitud_semilog_HG.png", dpi=150)

# 2) Posteriores (lineal)
plt.figure()
for i in range(5):
    ys = [U[t][i] for t in T]
    plt.plot(T, ys, label=labels[i])
plt.xlim(0, T_MAX)
plt.ylim(0.0, 1.0)
plt.xticks(T)
plt.yticks([i/10 for i in range(0, 11)])
plt.xlabel("Número de tornillos extraídos (t)")
plt.ylabel("Probabilidad a posteriori P(h | t éxitos OBS)")
plt.title("Evolución de las probabilidades a posteriori (lineal)")
plt.grid(True)
plt.legend(loc="best")
plt.tight_layout()
plt.savefig("/mnt/data/posteriores_lineal_HG.png", dpi=150)

t_final = T_MAX
map_idx = max(range(5), key=lambda i: U[t_final][i])
resumen = {
    "OBS": OBS,
    "Ks": Ks,
    "t_final": t_final,
    "MAP_idx": map_idx,
    "MAP_label": labels[map_idx],
    "posterior_MAP": U[t_final][map_idx],
    "alpha_final": alpha[t_final],
}
resumen
