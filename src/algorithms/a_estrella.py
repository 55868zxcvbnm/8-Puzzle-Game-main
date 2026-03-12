"""
Algoritmo de Búsqueda A* (A-Estrella)

A* es un algoritmo de búsqueda informada que usa una función heurística
para guiar la búsqueda hacia el objetivo. Es completo y óptimo cuando
la heurística es admisible.

Función de costo: f(n) = g(n) + h(n)
- g(n): Costo del camino desde el nodo inicial hasta n
- h(n): Estimación heurística del costo desde n hasta el objetivo

Este módulo contiene:
- Función a_estrella: Implementación principal del algoritmo
"""

import heapq

from src.utils import NodoTablero


def a_estrella(nodo_inicial):
    """
    Algoritmo de búsqueda A* (A-Estrella).
    
    A* explora los nodos ordenados por su costo total f(n) = g(n) + h(n).
    Garantiza encontrar la solución óptima cuando la heurística es admisible.
    
    Args:
        nodo_inicial: NodoTablero con el estado inicial del puzzle
        
    Returns:
        Tupla con:
        - nodo_final: Nodo objetivo encontrado (o None si no hay solución)
        - nodos_expandidos: Cantidad de nodos expandidos durante la búsqueda
        - profundidad_maxima: Profundidad máxima alcanzada en el árbol de búsqueda
        
    Funcionamiento:
        1. Usar una priority queue (heap) ordenada por el costo f(n)
        2. Siempre expandir el nodo con menor costo primero
        3. Mantener un conjunto de estados explorados para evitar ciclos
    """
    # Cola de prioridad para la frontera
    # heapq mantiene el elemento con menor costo al frente
    frontera = []

    # Conjunto de estados ya explorados
    nodos_explorados = set()

    # Contadores
    nodos_expandidos = 0
    profundidad_maxima = 0

    # Insertar el nodo inicial en la frontera
    heapq.heappush(frontera, nodo_inicial)

    # Bucle principal
    while frontera:
        # Sacar el nodo con menor costo de la frontera
        nodo = heapq.heappop(frontera)

        # Marcar como explorado
        nodos_explorados.add(nodo.estado)

        # Verificar si es el objetivo
        if nodo.es_objetivo():
            return nodo, nodos_expandidos, profundidad_maxima

        # Expandir el nodo (generar hijos)
        nodo.expandir()
        nodos_expandidos += 1

        # Procesar cada hijo
        for vecino in nodo.nodos:
            # Solo agregar si no ha sido explorado
            if vecino.estado not in nodos_explorados:
                heapq.heappush(frontera, vecino)
                nodos_explorados.add(vecino.estado)

                # Actualizar profundidad máxima
                if vecino.profundidad > profundidad_maxima:
                    profundidad_maxima = vecino.profundidad

    # No se encontró solución
    return None, nodos_expandidos, profundidad_maxima

