"""
Algoritmo de Búsqueda en Anchura (BFS - Breadth-First Search)

BFS explora uniformemente todos los nodos al mismo nivel de profundidad
antes de pasar al siguiente nivel. Garantiza encontrar la solución óptima
en términos de número de movimientos, pero puede ser muy lento.

Este módulo contiene:
- Función bfs: Implementación principal del algoritmo de búsqueda en anchura
"""

from collections import deque

from src.utils import NodoTablero


def bfs(nodo_inicial):
    """
    Algoritmo de búsqueda en anchura (BFS).
    BFS explora todos los nodos a una profundidad d antes de explorar
    los nodos a profundidad d+1. Garantiza la solución más corta
    (menor número de movimientos) pero puede ser computacionalmente
    costoso para estados complejos.
    Args:
        nodo_inicial: NodoTablero con el estado inicial del puzzle
    Returns:
        Tupla con:
        - nodo_final: Nodo objetivo encontrado (o None si no hay solución)
        - nodos_expandidos: Cantidad de nodos expandidos durante la búsqueda
        - profundidad_maxima: Profundidad máxima alcanzada en el árbol de búsqueda
    Funcionamiento:
        1. Usar una cola (FIFO) para la frontera
        2. Siempre expandir el nodo más antiguo en la frontera
        3. Mantener un conjunto de estados explorados para evitar ciclos
    """
    # Cola FIFO para la frontera
    # deque es más eficiente que list para operaciones popleft
    frontera = deque()

    # Conjunto de estados ya explorados
    nodos_explorados = set()

    # Contadores
    nodos_expandidos = 0
    profundidad_maxima = 0

    # Insertar el nodo inicial al final de la cola
    frontera.append(nodo_inicial)

    # Bucle principal
    while frontera:
        # Sacar el nodo más antiguo de la frontera
        nodo = frontera.popleft()

        # Marcar como explorado
        nodos_explorados.add(nodo.estado)

        # Verificar si es el objetivo
        if nodo.es_objetivo():
            return nodo, nodos_expandidos, profundidad_maxima

        # Expandir el nodo
        nodo.expandir()
        nodos_expandidos += 1

        # Procesar cada hijo
        for vecino in nodo.nodos:
            # Solo agregar si no ha sido explorado
            if vecino.estado not in nodos_explorados:
                frontera.append(vecino)
                nodos_explorados.add(vecino.estado)

                # Actualizar profundidad máxima
                if vecino.profundidad > profundidad_maxima:
                    profundidad_maxima = vecino.profundidad

    # No se encontró solución
    return None, nodos_expandidos, profundidad_maxima
