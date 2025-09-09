# --- Definición de Probabilidades ---
# Probabilidades a priori de la avería
p_averia = {
    'electrica': 1e-3,
    'mecanica': 1e-5,
    'no_averia': 1 - 1e-3 - 1e-5
}

# Probabilidades condicionales de la temperatura
p_temp_dado_averia = {
    'no_averia': {'elevada': 0.17, 'reducida': 0.05, 'normal': 0.78},
    'electrica': {'elevada': 0.90, 'reducida': 0.01, 'normal': 0.09},
    'mecanica': {'elevada': 0.10, 'reducida': 0.40, 'normal': 0.50}
}

# Probabilidades condicionales del piloto
p_piloto_dado_temp = {
    'elevada': {'encendido': 0.95, 'apagado': 0.05},
    'reducida': {'encendido': 0.99, 'apagado': 0.01},
    'normal': {'encendido': 1e-6, 'apagado': 1 - 1e-6}
}

def calcular_prob_conjunta(averia, temp, piloto):
    """Calcula la probabilidad conjunta P(Averia, Temperatura, Piloto)."""
    return (p_piloto_dado_temp[temp][piloto] *
            p_temp_dado_averia[averia][temp] *
            p_averia[averia])

# --- Lógica de Cálculo y Presentación ---

print("## Análisis de la Red Bayesiana del Motor")
print("-------------------------------------------------------------------------------------------------------------")

# --- 3.1: Cálculo de P(Averia=mecanica | Piloto=encendido) ---
num_3_1 = sum(calcular_prob_conjunta('mecanica', temp, 'encendido')
            for temp in ['elevada', 'reducida', 'normal'])
den_3_1 = sum(calcular_prob_conjunta(averia, temp, 'encendido')
            for averia in ['electrica', 'mecanica', 'no_averia']
            for temp in ['elevada', 'reducida', 'normal'])

prob_3_1 = num_3_1 / den_3_1

print("### 📊 Resultado 3.1: Probabilidad de Avería Mecánica dado que el Piloto está Encendido")
print(f"Probabilidad Calculada: **{prob_3_1:.10f}**")
print("---------------------------------------------------------------------------------------------------------")

# --- 3.2: Cálculo de P(Averia=mecanica | Piloto=encendido, Temperatura=elevada) ---
num_3_2 = calcular_prob_conjunta('mecanica', 'elevada', 'encendido')
den_3_2 = sum(calcular_prob_conjunta(averia, 'elevada', 'encendido')
            for averia in ['electrica', 'mecanica', 'no_averia'])

prob_3_2 = num_3_2 / den_3_2

print("### 💡 Resultado 3.2: Probabilidad de Avería Mecánica dado que el Piloto está Encendido y la Temperatura es Elevada")
print(f"Probabilidad Calculada: **{prob_3_2:.10f}**")
print("---------------------------------------------------------------------------------------------------------")