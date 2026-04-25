import pygame
import networkx as nx
from nodo import Nodo
from arista import Arista
import config

class GrafoVisual:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.nodos = []
        self.aristas = []
        self.nodo_contador = 0
        self.modo = "agregar_nodo"  
        self.nodo_seleccionado = None
        self.nodo_inicio = None  
        self.nodo_fin = None     
        self.grafo_nx = nx.Graph()
        
    def agregar_nodo(self, x, y):
        for nodo in self.nodos:
            dx = nodo.x - x
            dy = nodo.y - y
            if (dx**2 + dy**2) ** 0.5 < nodo.radio * 2:
                return False
        
        nuevo_nodo = Nodo(x, y, self.nodo_contador)
        self.nodos.append(nuevo_nodo)
        self.grafo_nx.add_node(nuevo_nodo.id)
        self.nodo_contador += 1
        return True
    
    def agregar_arista(self, nodo1, nodo2, peso=1):
        # Verificar si ya existe
        for arista in self.aristas:
            if (arista.nodo1 == nodo1 and arista.nodo2 == nodo2) or \
               (arista.nodo1 == nodo2 and arista.nodo2 == nodo1):
                return False
        
        nueva_arista = Arista(nodo1, nodo2, peso)
        self.aristas.append(nueva_arista)
        self.grafo_nx.add_edge(nodo1.id, nodo2.id, weight=peso)
        return True
    
    def encontrar_nodo_por_posicion(self, x, y):
        for nodo in self.nodos:
            if nodo.contiene_punto(x, y):
                return nodo
        return None
    
    def dijkstra(self, inicio_id, fin_id):
        """Encuentra el camino más corto usando NetworkX"""
        try:
            camino = nx.dijkstra_path(self.grafo_nx, inicio_id, fin_id, weight='weight')
            longitud = nx.dijkstra_path_length(self.grafo_nx, inicio_id, fin_id, weight='weight')
            return camino, longitud
        except nx.NetworkXNoPath:
            return None, None
    
    def arbol_expansion_minima(self):
        """Encuentra el MST usando Prim o Kruskal"""
        if len(self.nodos) == 0:
            return None
        
        # Verificar si el grafo es conexo
        if not nx.is_connected(self.grafo_nx):
            return None
        
        mst = nx.minimum_spanning_tree(self.grafo_nx, weight='weight')
        return mst
    
    def dibujar(self, pantalla):
        pantalla.fill(config.COLORES['BLANCO'])
        
        for arista in self.aristas:
            arista.dibujar(pantalla)
        
        for nodo in self.nodos:
            nodo.dibujar(pantalla)
        
        fuente = pygame.font.Font(None, 30)
        texto = fuente.render(f"Modo: {self.modo}", True, config.COLORES['NEGRO'])
        pantalla.blit(texto, (10, 10))
        
        self.mostrar_ayuda(pantalla)
    
    def mostrar_ayuda(self, pantalla):
        fuente = pygame.font.Font(None, 20)
        ayudas = [
            "1: Modo Agregar Nodo | 2: Modo Agregar Arista | 3: Modo Mover/Eliminar",
            "Click izquierdo: Agregar/Mover/Eliminar | Click derecho: Seleccionar inicio/fin",
            "D: Calcular camino más corto | M: Calcular árbol de expansión mínima",
            "C: Limpiar selección | ESC: Limpiar todo"
        ]
        
        for i, ayuda in enumerate(ayudas):
            texto = fuente.render(ayuda, True, config.COLORES['GRIS'])
            pantalla.blit(texto, (10, self.alto - 80 + i * 20))
    

    def limpiar_seleccion_arista(self):
        """Limpia la selección temporal de arista"""
        if hasattr(self, 'nodo_arista_temporal') and self.nodo_arista_temporal:
            self.nodo_arista_temporal.color = config.COLORES['AZUL']
            self.nodo_arista_temporal = None