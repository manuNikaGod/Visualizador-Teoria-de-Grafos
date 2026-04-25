import pygame
import config

class AlgoritmosVisuales:
    @staticmethod
    def visualizar_camino(grafo_visual, pantalla, camino_ids, duracion=2.0):
        """Visualiza el camino más corto de forma animada"""
        if not camino_ids:
            return
        
        nodos_camino = [n for n in grafo_visual.nodos if n.id in camino_ids]
        
        reloj = pygame.time.Clock()
        tiempo_inicio = pygame.time.get_ticks()
        
        while (pygame.time.get_ticks() - tiempo_inicio) / 1000.0 < duracion:
            grafo_visual.dibujar(pantalla)
            
            # Dibujar aristas del camino en verde
            for i in range(len(camino_ids) - 1):
                nodo_actual = next(n for n in grafo_visual.nodos if n.id == camino_ids[i])
                nodo_siguiente = next(n for n in grafo_visual.nodos if n.id == camino_ids[i+1])
                
                for arista in grafo_visual.aristas:
                    if (arista.nodo1 == nodo_actual and arista.nodo2 == nodo_siguiente) or \
                       (arista.nodo1 == nodo_siguiente and arista.nodo2 == nodo_actual):
                        arista.color = config.COLORES['VERDE']
                        arista.grosor = 4
                        arista.dibujar(pantalla)
                        break
            
            for nodo in nodos_camino:
                nodo.color = config.COLORES['VERDE']
                nodo.dibujar(pantalla)
            
            pygame.display.flip()
            reloj.tick(60)
        
        for arista in grafo_visual.aristas:
            arista.color = config.COLORES['NEGRO']
            arista.grosor = 2
        for nodo in grafo_visual.nodos:
            if nodo != grafo_visual.nodo_inicio and nodo != grafo_visual.nodo_fin:
                nodo.color = config.COLORES['AZUL']
    
    @staticmethod
    def visualizar_mst(grafo_visual, pantalla, mst_nx, duracion=2.0):
        """Visualiza el árbol de expansión mínima"""
        if not mst_nx or mst_nx.number_of_edges() == 0:
            return
        
        reloj = pygame.time.Clock()
        tiempo_inicio = pygame.time.get_ticks()
        
        while (pygame.time.get_ticks() - tiempo_inicio) / 1000.0 < duracion:
            grafo_visual.dibujar(pantalla)
            
            for u, v, data in mst_nx.edges(data=True):
                nodo_u = next(n for n in grafo_visual.nodos if n.id == u)
                nodo_v = next(n for n in grafo_visual.nodos if n.id == v)
                
                for arista in grafo_visual.aristas:
                    if (arista.nodo1 == nodo_u and arista.nodo2 == nodo_v) or \
                       (arista.nodo1 == nodo_v and arista.nodo2 == nodo_u):
                        arista.color = config.COLORES['MORADO']
                        arista.grosor = 4
                        arista.dibujar(pantalla)
                        break
            
            pygame.display.flip()
            reloj.tick(60)
        
        # Restaurar colores
        for arista in grafo_visual.aristas:
            arista.color = config.COLORES['NEGRO']
            arista.grosor = 2