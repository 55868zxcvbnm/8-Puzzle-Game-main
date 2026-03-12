"""
Módulo de Funciones Heurísticas

Este módulo contiene las funciones heurísticas utilizadas por los
algoritmos de búsqueda para estimar el costo hasta el objetivo.

La heurística es una estimación de qué tan "lejos" está un estado
del estado objetivo. Una buena heurística debe ser:
- Admisible: nunca sobreestima el costo real
- Consistente: cumple la desigualdad triangular
"""

from src.core.tablero import Tablero


def distancia_manhattan(x1, y1, x2, y2):
    """
    Calcula la distancia Manhattan entre dos puntos.
    
    La distancia Manhattan es la suma de las diferencias absolutas
    de sus coordenadas cartesianas. Es la heurística más común
    para el 8-Puzzle porque representa el mínimo número de
    movimientos necesarios si las losetas pudieran moverse
    directamente a su posición objetivo.
    
    Args:
        x1, y1: Coordenadas del primer punto
        x2, y2: Coordenadas del segundo punto
        
    Returns:
        Distancia Manhattan (entero)
        
    Ejemplo:
        punto A(0,0) a punto B(2,1) -> |0-2| + |0-1| = 2 + 1 = 3
    """
    return abs(x1 - x2) + abs(y1 - y2)


def distancia_manhattan_tablero(estado, objetivo=None):
    """
    Calcula la distancia Manhattan total para todo el tablero.
    
    Suma la distancia Manhattan de cada número desde su posición
    actual hasta su posición objetivo.
    
    Args:
        estado: Tupla de 9 elementos con el estado actual
        objetivo: Tupla de 9 elementos con el estado objetivo (opcional)
                  Por defecto es (0,1,2,3,4,5,6,7,8)
        
    Returns:
        Distancia Manhattan total del tablero (entero)
    """
    if objetivo is None:
        objetivo = Tablero.ESTADO_OBJETIVO
    
    suma = 0
    for indice, elemento in enumerate(estado):
        if elemento != 0:  # Ignorar el espacio en blanco
            # Coordenadas actuales
            x_actual, y_actual = Tablero.traducir_a_2d(indice)
            
            # Coordenadas objetivo del elemento
            x_objetivo, y_objetivo = Tablero.traducir_a_2d(objetivo.index(elemento))
            
            # Sumar distancia Manhattan
            suma += distancia_manhattan(x_actual, y_actual, x_objetivo, y_objetivo)
    
    return suma


def heuristica_blancos_incorrectos(estado, objetivo=None):
    """
    Cuenta cuántos números están en la posición incorrecta.
    
    Esta heurística es más simple pero menos precisa que
    la distancia Manhattan. Solo cuenta cuántos elementos
    NO están en su posición objetivo.
    
    Args:
        estado: Tupla de 9 elementos
        objetivo: Tupla objetivo (opcional)
        
    Returns:
        Número de elementos fuera de lugar (entero)
    """
    if objetivo is None:
        objetivo = Tablero.ESTADO_OBJETIVO
    
    contador = 0
    for i in range(9):
        if estado[i] != 0 and estado[i] != objetivo[i]:
            contador += 1
    
    return contador


# ==============================================================================
# EXPORTS
# ==============================================================================

__all__ = [
    'distancia_manhattan',
    'distancia_manhattan_tablero',
    'heuristica_blancos_incorrectos'
]

