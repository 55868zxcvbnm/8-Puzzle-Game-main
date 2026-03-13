"""
Módulo de utilidades del juego 8-Puzzle

Este módulo existe para compatibilidad con código existente.
Las clases y funciones reales están en el paquete src/core/
"""

from src.core import (
    Tablero,
    Nodo,
    NodoTablero,
    distancia_manhattan,
    Algorithm
)

__all__ = ['Tablero', 'Nodo', 'NodoTablero', 'distancia_manhattan', 'Algorithm']
