"""
Paquete de Nucleo (Core)

Este paquete contiene la lógica base del juego:
- tablero.py: Operaciones del tablero
- nodos.py: Clases Nodo para búsqueda
- heuristica.py: Funciones heurísticas
"""

from src.core.tablero import Tablero, Algorithm
from src.core.nodos import Nodo, NodoTablero
from src.core.heuristica import distancia_manhattan

__all__ = ['Tablero', 'Nodo', 'NodoTablero', 'distancia_manhattan', 'Algorithm']

