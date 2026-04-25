# main.py - VERSIÓN CORREGIDA (sin diálogo bloqueante)

import pygame
import sys
from grafo_visual import GrafoVisual
from algoritmos import AlgoritmosVisuales
import config

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((config.ANCHO_VENTANA, config.ALTO_VENTANA))
    pygame.display.set_caption("Visualizador Interactivo de Teoría de Grafos")
    config.FUENTE = pygame.font.Font(None, 36)
    
    grafo = GrafoVisual(config.ANCHO_VENTANA, config.ALTO_VENTANA)
    reloj = pygame.time.Clock()
    
    # Variables de estado
    nodo_arista_temporal = None
    entrada_peso = ""
    pidiendo_peso = False
    nodo_destino_peso = None
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Manejo de teclado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    grafo.modo = "agregar_nodo"
                    pidiendo_peso = False  # Cancelar entrada de peso
                    nodo_arista_temporal = None
                elif evento.key == pygame.K_2:
                    grafo.modo = "agregar_arista"
                    pidiendo_peso = False
                    nodo_arista_temporal = None
                elif evento.key == pygame.K_3:
                    grafo.modo = "mover_eliminar"
                    pidiendo_peso = False
                    nodo_arista_temporal = None
                elif evento.key == pygame.K_d:
                    if grafo.nodo_inicio and grafo.nodo_fin:
                        camino, longitud = grafo.dijkstra(
                            grafo.nodo_inicio.id, 
                            grafo.nodo_fin.id
                        )
                        if camino:
                            print(f"Camino encontrado: {camino} (Longitud: {longitud})")
                            AlgoritmosVisuales.visualizar_camino(grafo, pantalla, camino)
                        else:
                            print("No hay camino entre los nodos seleccionados")
                elif evento.key == pygame.K_m:
                    mst = grafo.arbol_expansion_minima()
                    if mst:
                        print(f"MST encontrado con {mst.number_of_edges()} aristas")
                        AlgoritmosVisuales.visualizar_mst(grafo, pantalla, mst)
                    else:
                        print("No se puede calcular MST (grafo no conexo o vacío)")
                elif evento.key == pygame.K_c:
                    grafo.nodo_inicio = None
                    grafo.nodo_fin = None
                    if grafo.nodo_seleccionado:
                        grafo.nodo_seleccionado.seleccionado = False
                        grafo.nodo_seleccionado = None
                    pidiendo_peso = False
                    nodo_arista_temporal = None
                elif evento.key == pygame.K_ESCAPE:
                    grafo.nodos.clear()
                    grafo.aristas.clear()
                    grafo.nodo_contador = 0
                    grafo.grafo_nx.clear()
                    pidiendo_peso = False
                    nodo_arista_temporal = None
                
                # Manejar entrada de peso (solo si estamos pidiendo peso)
                if pidiendo_peso:
                    if evento.key == pygame.K_RETURN:
                        if entrada_peso:
                            try:
                                peso = int(entrada_peso)
                            except ValueError:
                                peso = 1
                            # Crear la arista
                            if nodo_arista_temporal and nodo_destino_peso:
                                grafo.agregar_arista(nodo_arista_temporal, nodo_destino_peso, peso)
                                # Restaurar color del nodo temporal
                                nodo_arista_temporal.color = config.COLORES['AZUL']
                        # Salir del modo entrada de peso
                        pidiendo_peso = False
                        nodo_arista_temporal = None
                        nodo_destino_peso = None
                        entrada_peso = ""
                    elif evento.key == pygame.K_BACKSPACE:
                        entrada_peso = entrada_peso[:-1]
                    elif evento.key == pygame.K_ESCAPE:
                        # Cancelar
                        pidiendo_peso = False
                        if nodo_arista_temporal:
                            nodo_arista_temporal.color = config.COLORES['AZUL']
                        nodo_arista_temporal = None
                        nodo_destino_peso = None
                        entrada_peso = ""
                    elif evento.unicode.isdigit():
                        entrada_peso += evento.unicode
            
            # Manejo de mouse (solo si NO estamos en modo entrada de peso)
            if evento.type == pygame.MOUSEBUTTONDOWN and not pidiendo_peso:
                x, y = pygame.mouse.get_pos()
                
                # Panel derecho para controles (área no interactiva)
                if x > 900:
                    continue
                
                if evento.button == 1:  # Click izquierdo
                    if grafo.modo == "agregar_nodo":
                        grafo.agregar_nodo(x, y)
                    
                    elif grafo.modo == "agregar_arista":
                        nodo_click = grafo.encontrar_nodo_por_posicion(x, y)
                        if nodo_click:
                            if nodo_arista_temporal is None:
                                # Primer nodo seleccionado
                                nodo_arista_temporal = nodo_click
                                nodo_click.color = config.COLORES['NARANJA']
                            else:
                                # Segundo nodo seleccionado
                                if nodo_arista_temporal != nodo_click:
                                    # Evitar aristas duplicadas
                                    arista_existe = False
                                    for arista in grafo.aristas:
                                        if (arista.nodo1 == nodo_arista_temporal and arista.nodo2 == nodo_click) or \
                                           (arista.nodo1 == nodo_click and arista.nodo2 == nodo_arista_temporal):
                                            arista_existe = True
                                            break
                                    
                                    if not arista_existe:
                                        # Solicitar peso (modo no bloqueante)
                                        pidiendo_peso = True
                                        nodo_destino_peso = nodo_click
                                        entrada_peso = "1"  # Peso por defecto
                                    else:
                                        # Ya existe, cancelar selección
                                        nodo_arista_temporal.color = config.COLORES['AZUL']
                                        nodo_arista_temporal = None
                                else:
                                    # Mismo nodo, cancelar
                                    nodo_arista_temporal.color = config.COLORES['AZUL']
                                    nodo_arista_temporal = None
                    
                    elif grafo.modo == "mover_eliminar":
                        nodo_click = grafo.encontrar_nodo_por_posicion(x, y)
                        if nodo_click:
                            # Eliminar nodo y sus aristas
                            aristas_a_eliminar = [a for a in grafo.aristas 
                                                if a.nodo1 == nodo_click or a.nodo2 == nodo_click]
                            for arista in aristas_a_eliminar:
                                grafo.aristas.remove(arista)
                                grafo.grafo_nx.remove_edge(arista.nodo1.id, arista.nodo2.id)
                            
                            grafo.nodos.remove(nodo_click)
                            grafo.grafo_nx.remove_node(nodo_click.id)
                
                elif evento.button == 3:  # Click derecho - seleccionar inicio/fin
                    nodo_click = grafo.encontrar_nodo_por_posicion(x, y)
                    if nodo_click:
                        if grafo.nodo_inicio is None:
                            grafo.nodo_inicio = nodo_click
                            nodo_click.color = config.COLORES['VERDE']
                        elif grafo.nodo_fin is None and nodo_click != grafo.nodo_inicio:
                            grafo.nodo_fin = nodo_click
                            nodo_click.color = config.COLORES['ROJO']
                        else:
                            # Limpiar selecciones
                            if grafo.nodo_inicio:
                                grafo.nodo_inicio.color = config.COLORES['AZUL']
                            if grafo.nodo_fin:
                                grafo.nodo_fin.color = config.COLORES['AZUL']
                            grafo.nodo_inicio = nodo_click
                            grafo.nodo_fin = None
                            nodo_click.color = config.COLORES['VERDE']
        
        # Dibujar todo
        grafo.dibujar(pantalla)
        
        # Mostrar cuadro de entrada de peso si está activo
        if pidiendo_peso:
            # Fondo semitransparente
            s = pygame.Surface((config.ANCHO_VENTANA, config.ALTO_VENTANA), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            pantalla.blit(s, (0, 0))
            
            # Cuadro de diálogo
            cuadro_ancho = 400
            cuadro_alto = 150
            cuadro_x = (config.ANCHO_VENTANA - cuadro_ancho) // 2
            cuadro_y = (config.ALTO_VENTANA - cuadro_alto) // 2
            
            pygame.draw.rect(pantalla, config.COLORES['BLANCO'], (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
            pygame.draw.rect(pantalla, config.COLORES['NEGRO'], (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), 3)
            
            # Texto
            fuente_grande = pygame.font.Font(None, 28)
            texto_pregunta = fuente_grande.render("Peso de la arista:", True, config.COLORES['NEGRO'])
            pantalla.blit(texto_pregunta, (cuadro_x + 20, cuadro_y + 30))
            
            # Caja de entrada
            caja_input_x = cuadro_x + 20
            caja_input_y = cuadro_y + 70
            caja_input_ancho = 200
            caja_input_alto = 40
            
            pygame.draw.rect(pantalla, config.COLORES['BLANCO'], (caja_input_x, caja_input_y, caja_input_ancho, caja_input_alto))
            pygame.draw.rect(pantalla, config.COLORES['NEGRO'], (caja_input_x, caja_input_y, caja_input_ancho, caja_input_alto), 2)
            
            texto_peso = fuente_grande.render(entrada_peso, True, config.COLORES['NEGRO'])
            pantalla.blit(texto_peso, (caja_input_x + 10, caja_input_y + 8))
            
            # Instrucciones
            fuente_pequeña = pygame.font.Font(None, 18)
            instrucciones = fuente_pequeña.render("Enter: Aceptar | ESC: Cancelar", True, config.COLORES['GRIS'])
            pantalla.blit(instrucciones, (cuadro_x + 20, cuadro_y + 120))
        
        # Dibujar panel de control lateral
        pygame.draw.rect(pantalla, (240, 240, 240), (900, 0, 300, config.ALTO_VENTANA))
        pygame.draw.line(pantalla, config.COLORES['NEGRO'], (900, 0), (900, config.ALTO_VENTANA), 2)
        
        fuente = pygame.font.Font(None, 24)
        
        controles = [
            "CONTROLES:",
            "",
            "1 - Agregar Nodo",
            "2 - Agregar Arista",
            "3 - Mover/Eliminar",
            "",
            "Click derecho:",
            "  Inicio/Fin ruta",
            "",
            "D - Dijkstra",
            "M - Árbol Mínimo",
            "C - Limpiar selección",
            "ESC - Limpiar todo",
            "",
            f"MODO ACTUAL:",
            f"  {grafo.modo}"
        ]
        
        for i, control in enumerate(controles):
            if "MODO ACTUAL:" in control:
                color = config.COLORES['AZUL']
            elif grafo.modo in control and "  " in control:
                color = config.COLORES['VERDE']
            else:
                color = config.COLORES['NEGRO']
            texto = fuente.render(control, True, color)
            pantalla.blit(texto, (920, 30 + i * 28))
        
        # Mostrar nodos seleccionados para Dijkstra
        if grafo.nodo_inicio or grafo.nodo_fin:
            y_offset = 30 + len(controles) * 28 + 20
            if grafo.nodo_inicio:
                texto = fuente.render(f"Inicio: Nodo {grafo.nodo_inicio.id}", True, config.COLORES['VERDE'])
                pantalla.blit(texto, (920, y_offset))
                y_offset += 28
            if grafo.nodo_fin:
                texto = fuente.render(f"Destino: Nodo {grafo.nodo_fin.id}", True, config.COLORES['ROJO'])
                pantalla.blit(texto, (920, y_offset))
        
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()