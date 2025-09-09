# =========================================================
# Ejercicio de Probabilidad y Regla de Bayes: Fábrica de Clavos
# =========================================================

# 1. Definición de las probabilidades a priori (producción de cada máquina)
P_M1 = 0.30  # Probabilidad de que un clavo sea de la Máquina 1 (30%)
P_M2 = 0.70  # Probabilidad de que un clavo sea de la Máquina 2 (70%)

# 2. Definición de las probabilidades condicionales (defectuoso dado la máquina)
P_D_dado_M1 = 0.02  # Probabilidad de ser defectuoso dado que es de M1 (2%)
P_D_dado_M2 = 0.03  # Probabilidad de ser defectuoso dado que es de M2 (3%)

# 3. Aplicación de la Ley de la Probabilidad Total
# Calculamos P(D): Probabilidad total de que un clavo sea defectuoso
# P(D) = P(D|M1) * P(M1) + P(D|M2) * P(M2)
P_D = (P_D_dado_M1 * P_M1) + (P_D_dado_M2 * P_M2)

# 4. Aplicación de la Regla de Bayes
# Buscamos P(M1|D): Probabilidad de que sea de la Máquina 1, dado que es defectuoso.
# P(M1|D) = [P(D|M1) * P(M1)] / P(D)
numerador_bayes = P_D_dado_M1 * P_M1
P_M1_dado_D = numerador_bayes / P_D

# 5. Impresión de Resultados
print(f"--- Probabilidades Iniciales ---")
print(f"Probabilidad de ser defectuoso de M1 (P(D|M1)): {P_D_dado_M1:.2f}")
print(f"Probabilidad de ser defectuoso de M2 (P(D|M2)): {P_D_dado_M2:.2f}")
print(f"Producción de M1 (P(M1)): {P_M1:.2f}")
print(f"Producción de M2 (P(M2)): {P_M2:.2f}")
print(f"--------------------------------")

print(f"\n--- Paso Intermedio: Ley de Probabilidad Total ---")
print(f"Probabilidad Total de un clavo defectuoso (P(D)): {P_D:.4f}")

print(f"\n--- Resultado Final: Regla de Bayes ---")
print(f"Probabilidad de que el clavo defectuoso sea de la Máquina 1 (P(M1|D)): {P_M1_dado_D:.4f}")
print(f"O en porcentaje: {P_M1_dado_D * 100:.2f}%")