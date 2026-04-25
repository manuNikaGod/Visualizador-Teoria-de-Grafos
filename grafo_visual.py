# grafo_visual.py
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
        # Evitar solapamiento
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
        """Encuentra el camino más corto usando NetworkX con validaciones"""
        # Validación 1: Verificar que existan nodos
        if len(self.nodos) < 2:
            print("❌ Error: Se necesitan al menos 2 nodos para calcular una ruta")
            return None, None
        
        # Validación 2: Verificar que los nodos existan
        nodos_ids = [n.id for n in self.nodos]
        if inicio_id not in nodos_ids:
            print(f"❌ Error: El nodo inicio {inicio_id} no existe")
            return None, None
        if fin_id not in nodos_ids:
            print(f"❌ Error: El nodo fin {fin_id} no existe")
            return None, None
        
        # Validación 3: Verificar que haya aristas
        if len(self.aristas) == 0:
            print("❌ Error: No hay aristas en el grafo")
            return None, None
        
        # Validación 4: Verificar conectividad
        if not nx.is_connected(self.grafo_nx):
            print("⚠️ Advertencia: El grafo no es conexo. Puede que no exista camino.")
        
        try:
            camino = nx.dijkstra_path(self.grafo_nx, inicio_id, fin_id, weight='weight')
            longitud = nx.dijkstra_path_length(self.grafo_nx, inicio_id, fin_id, weight='weight')
            print(f"✅ Camino encontrado: {camino} (Longitud total: {longitud})")
            return camino, longitud
        except nx.NetworkXNoPath:
            print(f"❌ Error: No existe camino entre el nodo {inicio_id} y {fin_id}")
            return None, None
        except Exception as e:
            print(f"❌ Error inesperado en Dijkstra: {e}")
            return None, None
    
    def arbol_expansion_minima(self):
        """Encuentra el MST usando Prim/Kruskal con validaciones"""
        # Validación 1: Verificar que haya nodos
        if len(self.nodos) == 0:
            print("❌ Error: No hay nodos en el grafo")
            return None
        
        # Validación 2: Verificar que haya al menos 2 nodos
        if len(self.nodos) < 2:
            print("❌ Error: Se necesitan al menos 2 nodos para formar un árbol")
            return None
        
        # Validación 3: Verificar que haya aristas suficientes
        if len(self.aristas) < len(self.nodos) - 1:
            print(f"❌ Error: Se necesitan al menos {len(self.nodos)-1} aristas para un árbol. Actual: {len(self.aristas)}")
            return None
        
        # Validación 4: Verificar conectividad
        if not nx.is_connected(self.grafo_nx):
            print("❌ Error: El grafo no es conexo. No se puede calcular el árbol de expansión mínima.")
            print("   Para calcular MST, el grafo debe estar completamente conectado.")
            return None
        
        try:
            mst = nx.minimum_spanning_tree(self.grafo_nx, weight='weight')
            peso_total = sum(data['weight'] for u, v, data in mst.edges(data=True))
            print(f"✅ MST calculado correctamente. Peso total: {peso_total}")
            print(f"   Aristas en MST: {list(mst.edges())}")
            return mst
        except Exception as e:
            print(f"❌ Error inesperado al calcular MST: {e}")
            return None
    
    def dibujar(self, pantalla):
        pantalla.fill(config.COLORES['BLANCO'])
        
        # Dibujar aristas
        for arista in self.aristas:
            arista.dibujar(pantalla)
        
        # Dibujar nodos
        for nodo in self.nodos:
            nodo.dibujar(pantalla)
        
        # Mostrar modo actual
        fuente = pygame.font.Font(None, 30)
        texto = fuente.render(f"Modo: {self.modo}", True, config.COLORES['NEGRO'])
        pantalla.blit(texto, (10, 10))
        
        # Mostrar ayuda
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