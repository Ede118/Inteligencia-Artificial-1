#El ejercicio no pide hacer esto pero quisimos hacerlo para divertirnos
import pygame
import sys
import time
import random

# Inicialización de Pygame
pygame.init()

# Definición de constantes
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 600
TAMANO_CELDA = ANCHO_PANTALLA // 4
FPS = 5

# Definición de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE_CLARO = (173, 255, 47)  # Casilla segura
AMARILLO_CLARO = (255, 255, 153) # Casilla visitada
ROJO = (255, 0, 0)
AZUL_CLARO = (173, 216, 230) # Casilla con brisa
NARANJA = (255, 165, 0) # Casilla con hedor
CYAN = (0, 255, 255) # Casilla con oro
VERDE_OSCURO = (0, 100, 0) # Wumpus muerto
GRIS_OSCURO = (50, 50, 50) # Agente muerto

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Agente IA en el Mundo de Wumpus (Disparo al Wumpus)")
reloj = pygame.time.Clock()

# Carga de fuente para el texto
fuente = pygame.font.Font(None, 24)

class Agente:
    def __init__(self):
        self.fila = 3
        self.columna = 0
        self.meta_alcanzada = False
        self.flechas = 1
        self.esta_vivo = True
        
        self.conocido = [[False for _ in range(4)] for _ in range(4)]
        self.es_segura = [[False for _ in range(4)] for _ in range(4)]
        self.ruta_visitada = [(3, 0)]
        self.posibles_pozos = []
        self.posibles_wumpus = []
        self.disparo_realizado = False

        self.es_segura[self.fila][self.columna] = True
        
    def mover_a(self, nueva_fila, nueva_columna):
        self.fila = nueva_fila
        self.columna = nueva_columna

    def obtener_vecinos(self, fila, columna):
        vecinos = []
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(movimientos)
        for dr, dc in movimientos:
            nueva_fila, nueva_columna = fila + dr, columna + dc
            if 0 <= nueva_fila < 4 and 0 <= nueva_columna < 4:
                vecinos.append((nueva_fila, nueva_columna))
        return vecinos

    def inferir_y_decidir(self, mundo_objetos):
        if not self.esta_vivo or self.meta_alcanzada:
            return False

        self.conocido[self.fila][self.columna] = True
        
        hay_brisa = (self.fila, self.columna) in mundo_objetos['brisa_casillas']
        hay_hedor = (self.fila, self.columna) in mundo_objetos['hedor_casillas']

        # CONDICIÓN DE DERROTA
        if (self.fila, self.columna) in mundo_objetos['pozos'] or \
           ((self.fila, self.columna) == mundo_objetos['wumpus'] and not mundo_objetos.get('wumpus_muerto', False)):
            self.esta_vivo = False
            return False
            
        # CONDICIÓN DE VICTORIA
        if (self.fila, self.columna) == mundo_objetos['oro']:
            self.meta_alcanzada = True
            return True

        # INFERENCIA LÓGICA
        if hay_brisa:
            for r, c in self.obtener_vecinos(self.fila, self.columna):
                if not self.conocido[r][c] and (r, c) not in self.posibles_pozos:
                    self.posibles_pozos.append((r, c))
        else:
            for r, c in self.obtener_vecinos(self.fila, self.columna):
                self.es_segura[r][c] = True
                if (r, c) in self.posibles_pozos:
                    self.posibles_pozos.remove((r, c))
        
        if hay_hedor and not mundo_objetos.get('wumpus_muerto', False):
            for r, c in self.obtener_vecinos(self.fila, self.columna):
                if not self.conocido[r][c] and (r, c) not in self.posibles_wumpus:
                    self.posibles_wumpus.append((r, c))
        else:
            for r, c in self.obtener_vecinos(self.fila, self.columna):
                if (r, c) in self.posibles_wumpus:
                    self.posibles_wumpus.remove((r, c))
        
        # LÓGICA DE DISPARO
        if len(self.posibles_wumpus) == 1 and self.flechas > 0 and not self.disparo_realizado:
            wumpus_loc = self.posibles_wumpus[0]
            # Si el wumpus está en un vecino no visitado, disparamos
            if not self.conocido[wumpus_loc[0]][wumpus_loc[1]]:
                mundo_objetos['wumpus_muerto'] = True
                self.flechas = 0
                self.disparo_realizado = True
                print("¡El agente ha disparado y matado al Wumpus! 🏹")
                self.posibles_wumpus = []
                self.es_segura[wumpus_loc[0]][wumpus_loc[1]] = True
                return True

        # ACTUAR (moverse o retroceder)
        vecinos_actuales = self.obtener_vecinos(self.fila, self.columna)
        candidatos = [(r, c) for r, c in vecinos_actuales if self.es_segura[r][c] and not self.conocido[r][c]]
        
        if candidatos:
            r_siguiente, c_siguiente = candidatos[0]
            self.mover_a(r_siguiente, c_siguiente)
            self.ruta_visitada.append((r_siguiente, c_siguiente))
            return True
        else:
            if len(self.ruta_visitada) > 1:
                self.ruta_visitada.pop()
                r_anterior, c_anterior = self.ruta_visitada[-1]
                self.mover_a(r_anterior, c_anterior)
                return True

        return False

def dibujar_tablero(mundo_objetos):
    for fila in range(4):
        for columna in range(4):
            rect = pygame.Rect(columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            
            color = BLANCO
            if (fila, columna) == mundo_objetos['oro']:
                color = CYAN
            elif (fila, columna) in agente.ruta_visitada:
                color = AMARILLO_CLARO
            elif agente.es_segura[fila][columna]:
                color = VERDE_CLARO

            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, NEGRO, rect, 1)

            if (fila, columna) == mundo_objetos['wumpus'] and not mundo_objetos.get('wumpus_muerto', False):
                texto = fuente.render("WUMPUS", True, NEGRO)
                pantalla.blit(texto, (columna * TAMANO_CELDA + 5, fila * TAMANO_CELDA + 5))
            if mundo_objetos.get('wumpus_muerto', False) and (fila, columna) == mundo_objetos['wumpus']:
                texto = fuente.render("💀", True, VERDE_OSCURO)
                pantalla.blit(texto, (columna * TAMANO_CELDA + 5, fila * TAMANO_CELDA + 5))
            if (fila, columna) in mundo_objetos['pozos']:
                texto = fuente.render("POZO", True, NEGRO)
                pantalla.blit(texto, (columna * TAMANO_CELDA + 5, fila * TAMANO_CELDA + 5))
            
            if agente.conocido[fila][columna]:
                if (fila, columna) in mundo_objetos['hedor_casillas']:
                    texto = fuente.render("Hedor", True, NARANJA)
                    pantalla.blit(texto, (columna * TAMANO_CELDA + 5, fila * TAMANO_CELDA + 25))
                if (fila, columna) in mundo_objetos['brisa_casillas']:
                    texto = fuente.render("Brisa", True, AZUL_CLARO)
                    pantalla.blit(texto, (columna * TAMANO_CELDA + 5, fila * TAMANO_CELDA + 45))

def dibujar_agente(agente):
    x = agente.columna * TAMANO_CELDA + TAMANO_CELDA // 2
    y = agente.fila * TAMANO_CELDA + TAMANO_CELDA // 2
    if agente.esta_vivo:
        pygame.draw.circle(pantalla, ROJO, (x, y), TAMANO_CELDA // 4)
    else:
        pygame.draw.circle(pantalla, GRIS_OSCURO, (x, y), TAMANO_CELDA // 4)


def generar_percepciones(mundo_objetos):
    mundo_objetos['brisa_casillas'] = []
    mundo_objetos['hedor_casillas'] = []
    
    agente_temporal = Agente()
    
    for pozo in mundo_objetos['pozos']:
        for vecino in agente_temporal.obtener_vecinos(pozo[0], pozo[1]):
            if vecino not in mundo_objetos['brisa_casillas']:
                mundo_objetos['brisa_casillas'].append(vecino)
                
    for vecino in agente_temporal.obtener_vecinos(mundo_objetos['wumpus'][0], mundo_objetos['wumpus'][1]):
        if vecino not in mundo_objetos['hedor_casillas']:
            mundo_objetos['hedor_casillas'].append(vecino)
    
    return mundo_objetos

# **Configuración de un mundo solucionable**
mundo_objetos = {
    'wumpus': (1, 0),
    'pozos': [(3, 2), (1, 2), (0, 3)],
    'oro': (1, 1)
}

mundo_objetos = generar_percepciones(mundo_objetos)

agente = Agente()

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    agente.inferir_y_decidir(mundo_objetos)
    
    if agente.meta_alcanzada:
        print("¡El agente ha encontrado el oro y ha resuelto el juego! 🎉")
        corriendo = False
        time.sleep(3)
    elif not agente.esta_vivo:
        print("¡El agente ha muerto! 💀")
        corriendo = False
        time.sleep(3)

    pantalla.fill(BLANCO)
    dibujar_tablero(mundo_objetos)
    dibujar_agente(agente)

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
sys.exit()