import random

#definimos las cajas (peso, precio)
cajas = [
    (300, 100),
    (200, 50),
    (450, 115),
    (145, 25),
    (664, 200),
    (90, 30),
    (150, 40),
    (355, 100),
    (401, 100),
    (395, 100)
]

peso_max = 1000
poblacion = 50
generaciones = 100
prob_mutacion = 0.1

def selec_poblacion(individuo):
    peso_total = sum(cajas[i][0] for i in range(len(cajas)) if individuo[i] == 1)
    valor_total = sum(cajas[i][1] for i in range(len(cajas)) if individuo[i] == 1)
    if peso_total > peso_max:
        return 0  # inválido
    return valor_total

# Creamos individuo aleatorio (10 bits)
def crear_individuo():
    return [random.randint(0, 1) for _ in range(len(cajas))]