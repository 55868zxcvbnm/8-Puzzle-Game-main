"""
Módulo de Algoritmos de Búsqueda para el 8-Puzzle

Este paquete contiene los algoritmos de búsqueda utilizados para resolver
el juego del 8-Puzzle automáticamente.

Algoritmos disponibles:
- a_estrella: Algoritmo A* (óptimo, usa g(n) + h(n))
- avara: Algoritmo Greedy/Búsqueda Voraz (rápido, solo h(n))
- bfs: Algoritmo de búsqueda en anchura (BFS)
"""

from src.algorithms.a_estrella import a_estrella
from src.algorithms.avara import avara
from src.algorithms.bfs import bfs

__all__ = ['a_estrella', 'avara', 'bfs']

