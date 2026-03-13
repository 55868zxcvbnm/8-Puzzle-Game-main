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
    Args:
        nodo_inicial: NodoTablero con el estado inicial del puzzle
    Returns:
        Tupla con:
        - nodo_final: Nodo objetivo encontrado (o None si no hay solución)
        - nodos_expandidos: Cantidad de nodos expandidos durante la búsqueda
        - profundidad_maxima: Profundidad máxima alcanzada en el árbol de búsqueda
    Funcionamiento:
        1. Usar una priority queue (heap) ordenada solo por heurística h(n)
        2. Siempre expandir el nodo que parezca más cercano al objetivo
        3. NO considera cuántos movimientos se han hecho (g(n))
    Diferencia con A*:
        - A*: f(n) = g(n) + h(n)  -> Garantiza solución óptima
        - avara: f(n) = h(n)       -> Rápido pero puede no ser óptimo
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
