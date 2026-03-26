"""
Algoritmo de Búsqueda Voraz (Greedy Best-First Search)

Greedy Best-First Search es un algoritmo de búsqueda informada que solo
considera la heurística h(n) para guiar la búsqueda, SIN tener en cuenta
el costo del camino g(n).

Es muy rápido pero NO garantiza encontrar la solución óptima.
Puede encontrar soluciones subóptimas (más movimientos de lo necesario).

Este módulo contiene:
- Función avara: Implementación principal del algoritmo de búsqueda voraz
"""

import heapq

from src.utils import NodoTablero


def avara(nodo_inicial):
    """
    Algoritmo de búsqueda voraz (Greedy Best-First Search).

    Avara explora los nodos ordenados solo por su heurística h(n),
    sin considerar la profundidad del nodo (g(n)).
    Es muy rápido pero puede encontrar soluciones subóptimas.
    """
    # Cola de prioridad para la frontera
    # Ordena solo por heurística (distancia Manhattan)
    frontera = []

    # Conjunto de estados ya explorados
    nodos_explorados = set()

    # Contadores
    nodos_expandidos = 0
    profundidad_maxima = 0

    # Insertar el nodo inicial en la frontera
    # Usamos una tupla (heuristica, nodo) para ordenar por heurística
    heapq.heappush(frontera, (nodo_inicial.heuristica_sola(), nodo_inicial))

    # Bucle principal
    while frontera:
        # Sacar el nodo con menor heurística de la frontera
        _, nodo = heapq.heappop(frontera)

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
                # Insertar con solo la heurística (sin profundidad)
                heapq.heappush(frontera, (vecino.heuristica_sola(), vecino))
                nodos_explorados.add(vecino.estado)

                # Actualizar profundidad máxima
                if vecino.profundidad > profundidad_maxima:
                    profundidad_maxima = vecino.profundidad

    # No se encontró solución
    return None, nodos_expandidos, profundidad_maxima
