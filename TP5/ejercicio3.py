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
    """
    Calcula la probabilidad conjunta P(Averia, Temperatura, Piloto)
    usando la regla de la cadena: P(P|T) * P(T|A) * P(A).
    """
    return (p_piloto_dado_temp[temp][piloto] *
            p_temp_dado_averia[averia][temp] *
            p_averia[averia])

# Problema 3.1: P(Avería=mecanica | Piloto=encendido) ---
print("## Resultado 3.1: Inferencia por Enumeración")
print("### P(Avería Mecánica | Piloto Encendido)")

# Numerador: P(Avería=mecanica, Piloto=encendido)
# Se suman las probabilidades conjuntas de todas las temperaturas para la avería mecánica
num_3_1 = sum(calcular_prob_conjunta('mecanica', temp, 'encendido')
            for temp in ['elevada', 'reducida', 'normal'])

# Denominador: P(Piloto=encendido) (Probabilidad total)
# Se suman las probabilidades conjuntas de todas las averías y temperaturas
den_3_1 = sum(calcular_prob_conjunta(averia, temp, 'encendido')
            for averia in ['electrica', 'mecanica', 'no_averia']
            for temp in ['elevada', 'reducida', 'normal'])

prob_3_1 = num_3_1 / den_3_1
print(f"Probabilidad Calculada: **{prob_3_1:.10f}**")
print(f"---------------------------------------------------------------------------------------------------")

# Problema 3.2: P(Avería=mecanica | Piloto=encendido, Temperatura=elevada) ---
print("\n## Resultado 3.2: Inferencia por Enumeración")
print("### P(Avería Mecánica | Piloto Encendido, Temperatura Elevada)")

# Numerador: P(Avería=mecanica, Temperatura=elevada, Piloto=encendido)
# No es necesario sumar porque la temperatura ya es un evento observado
num_3_2 = calcular_prob_conjunta('mecanica', 'elevada', 'encendido')

# Denominador: P(Temperatura=elevada, Piloto=encendido)
# Se suman las probabilidades conjuntas para cada tipo de avería
den_3_2 = sum(calcular_prob_conjunta(averia, 'elevada', 'encendido')
            for averia in ['electrica', 'mecanica', 'no_averia'])

prob_3_2 = num_3_2 / den_3_2
print(f"Probabilidad Calculada: **{prob_3_2:.10f}**")
print(f"---------------------------------------------------------------------------------------------------")