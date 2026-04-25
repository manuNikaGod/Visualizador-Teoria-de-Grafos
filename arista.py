# arista.py
import pygame
import config

class Arista:
    def __init__(self, nodo1, nodo2, peso=1):
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.peso = peso
        self.color = config.COLORES['NEGRO']
        self.grosor = 2
        
    def dibujar(self, pantalla):
        pygame.draw.line(pantalla, self.color, 
                        (self.nodo1.x, self.nodo1.y),
                        (self.nodo2.x, self.nodo2.y), 
                        self.grosor)
        
        # Dibujar peso en el medio
        medio_x = (self.nodo1.x + self.nodo2.x) // 2
        medio_y = (self.nodo1.y + self.nodo2.y) // 2
        
        fuente = pygame.font.Font(None, 20)
        texto = fuente.render(str(self.peso), True, config.COLORES['ROJO'])
        pantalla.blit(texto, (medio_x, medio_y))