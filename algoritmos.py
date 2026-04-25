import pygame
import config

class AlgoritmosVisuales:
    @staticmethod
    def visualizar_camino(grafo_visual, pantalla, camino_ids, duracion=2.0):
        """Visualiza el camino más corto de forma animada"""
        if not camino_ids or len(camino_ids) < 2:
            print("❌ No se puede visualizar: camino inválido")
            return
        
        # Guardar colores originales
        colores_originales_aristas = []
        for arista in grafo_visual.aristas:
            colores_originales_aristas.append((arista, arista.color, arista.grosor))
        
        colores_originales_nodos = []
        for nodo in grafo_visual.nodos:
            colores_originales_nodos.append((nodo, nodo.color))
        
        # Obtener nodos del camino
        nodos_camino = []
        for n in grafo_visual.nodos:
            if n.id in camino_ids:
                nodos_camino.append(n)
        
        reloj = pygame.time.Clock()
        tiempo_inicio = pygame.time.get_ticks()
        
        while (pygame.time.get_ticks() - tiempo_inicio) / 1000.0 < duracion:
            grafo_visual.dibujar(pantalla)
            
            # Dibujar aristas del camino en verde
            for i in range(len(camino_ids) - 1):
                nodo_actual = None
                nodo_siguiente = None
                for n in grafo_visual.nodos:
                    if n.id == camino_ids[i]:
                        nodo_actual = n
                    if n.id == camino_ids[i+1]:
                        nodo_siguiente = n
                
                if nodo_actual and nodo_siguiente:
                    for arista in grafo_visual.aristas:
                        if (arista.nodo1 == nodo_actual and arista.nodo2 == nodo_siguiente) or \
                           (arista.nodo1 == nodo_siguiente and arista.nodo2 == nodo_actual):
                            arista.color = config.COLORES['VERDE']
                            arista.grosor = 4
                            arista.dibujar(pantalla)
                            break
            
            # Dibujar nodos del camino en verde
            for nodo in nodos_camino:
                nodo.color = config.COLORES['VERDE']
                nodo.dibujar(pantalla)
            
            # Dibujar nodos inicio/fin con sus colores especiales
            if grafo_visual.nodo_inicio and grafo_visual.nodo_inicio not in nodos_camino:
                grafo_visual.nodo_inicio.dibujar(pantalla)
            if grafo_visual.nodo_fin and grafo_visual.nodo_fin not in nodos_camino:
                grafo_visual.nodo_fin.dibujar(pantalla)
            
            pygame.display.flip()
            reloj.tick(60)
        
        # RESTAURAR COLORES ORIGINALES DE LAS ARISTAS
        for arista, color_orig, grosor_orig in colores_originales_aristas:
            arista.color = color_orig
            arista.grosor = grosor_orig
        
        # RESTAURAR COLORES ORIGINALES DE LOS NODOS
        for nodo, color_orig in colores_originales_nodos:
            # No sobrescribir colores de inicio/fin
            if nodo != grafo_visual.nodo_inicio and nodo != grafo_visual.nodo_fin:
                nodo.color = color_orig
        
        # Asegurar colores correctos de inicio/fin
        if grafo_visual.nodo_inicio:
            grafo_visual.nodo_inicio.color = config.COLORES['VERDE']
        if grafo_visual.nodo_fin:
            grafo_visual.nodo_fin.color = config.COLORES['ROJO']
        
        # Forzar un redibujado final
        grafo_visual.dibujar(pantalla)
        pygame.display.flip()
    
    @staticmethod
    def visualizar_mst(grafo_visual, pantalla, mst_nx, duracion=2.0):
        """Visualiza el árbol de expansión mínima"""
        if not mst_nx or mst_nx.number_of_edges() == 0:
            print("❌ No hay MST para visualizar")
            return
        
        # Guardar colores originales de las aristas
        colores_originales = []
        for arista in grafo_visual.aristas:
            colores_originales.append((arista, arista.color, arista.grosor))
        
        reloj = pygame.time.Clock()
        tiempo_inicio = pygame.time.get_ticks()
        
        while (pygame.time.get_ticks() - tiempo_inicio) / 1000.0 < duracion:
            grafo_visual.dibujar(pantalla)
            
            # Resaltar aristas del MST
            for u, v, data in mst_nx.edges(data=True):
                # Buscar los nodos correspondientes
                nodo_u = None
                nodo_v = None
                for n in grafo_visual.nodos:
                    if n.id == u:
                        nodo_u = n
                    if n.id == v:
                        nodo_v = n
                
                if nodo_u and nodo_v:
                    for arista in grafo_visual.aristas:
                        if (arista.nodo1 == nodo_u and arista.nodo2 == nodo_v) or \
                           (arista.nodo1 == nodo_v and arista.nodo2 == nodo_u):
                            arista.color = config.COLORES['MORADO']
                            arista.grosor = 4
                            arista.dibujar(pantalla)
                            break
            
            pygame.display.flip()
            reloj.tick(60)
        
        # RESTAURAR COLORES ORIGINALES DE LAS ARISTAS
        for arista, color_orig, grosor_orig in colores_originales:
            arista.color = color_orig
            arista.grosor = grosor_orig
        
        # Forzar un redibujado final
        grafo_visual.dibujar(pantalla)
        pygame.display.flip()