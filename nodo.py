import pygame
import config

class Nodo:
    def __init__(self, x, y, id):
        self.x=x
        self.y=y
        self.id=id
        self.radio=config.RADIO_NODO
        self.color=config.COLORES["AZUL"]
        self.seleccionado=False
        
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (self.x, self.y), self.radio)
        pygame.draw.circle(pantalla,config.COLORES["NEGRO"], (self.x, self.y), self.radio, 2)
        
        fuente=pygame.font.Font(None, 24)
        texto=fuente.render(str(self.id), True, config.COLORES["NEGRO"])
        rect_texto=texto.get_rect(center=(self.x, self.y))
        pantalla.blit(texto, rect_texto)
        
        if self.seleccionado:
            pygame.draw.circle(pantalla, config.COLORES["AMARILLO"],
                               (self.x, self.y),
                               self.radio+5, 3)
    def contiene_punto(self, x,y):
        distacia=((self.x-x)**2+(self.y-y)**2)**0.5
        return distacia<=self.radio