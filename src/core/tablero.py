"""
Módulo de Operaciones del Tablero

Este módulo contiene la clase Tablero con todas las operaciones
relacionadas con el estado y manipulación del tablero del 8-Puzzle.
"""

import random
import time
from collections import namedtuple


class Tablero:
    """
    Clase estática que contiene todas las operaciones relacionadas con el tablero.
    No necesita ser instanciada, todos sus métodos son estáticos.
    """

    # Estado objetivo: (0,1,2,3,4,5,6,7,8)
    ESTADO_OBJETIVO = tuple(range(9))

    @staticmethod
    def traducir_a_2d(indice):
        """Convierte un índice 1D (0-8) a coordenadas 2D (fila, columna)."""
        return indice // 3, indice % 3

    @staticmethod
    def acciones_validas(estado):
        """Genera las acciones válidas que se pueden realizar desde un estado."""
        indice_vacio = estado.index(0)
        if indice_vacio > 2:
            yield 'U'
        if indice_vacio < 6:
            yield 'D'
        if indice_vacio % 3 > 0:
            yield 'L'
        if indice_vacio % 3 < 2:
            yield 'R'

    @staticmethod
    def transformar(estado, accion):
        """Aplica una acción al estado actual y retorna un nuevo estado."""
        estado = [*estado]
        indice_vacio = estado.index(0)

        match accion:
            case 'U':
                estado[indice_vacio], estado[indice_vacio - 3] = \
                    estado[indice_vacio - 3], estado[indice_vacio]
            case 'D':
                estado[indice_vacio], estado[indice_vacio + 3] = \
                    estado[indice_vacio + 3], estado[indice_vacio]
            case 'L':
                estado[indice_vacio], estado[indice_vacio - 1] = \
                    estado[indice_vacio - 1], estado[indice_vacio]
            case 'R':
                estado[indice_vacio], estado[indice_vacio + 1] = \
                    estado[indice_vacio + 1], estado[indice_vacio]

        return tuple(estado)

    @staticmethod
    def inversiones(estado):
        """Cuenta el número de inversiones en el estado."""
        suma_inversiones = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if estado[i] != 0 and estado[j] != 0 and estado[i] > estado[j]:
                    suma_inversiones += 1
        return suma_inversiones

    @staticmethod
    def es_resoluble(estado):
        """Verifica si un estado del tablero es resoluble."""
        return Tablero.inversiones(estado) % 2 == 0

    @staticmethod
    def crear_estado_resoluble():
        """Genera un estado aleatorio que es resoluble."""
        estado = [*range(9)]
        while True:
            random.shuffle(estado)
            if Tablero.es_resoluble(estado):
                return tuple(estado)

    @staticmethod
    def resolver(estado, func):
        """Resuelve un estado usando el algoritmo de búsqueda especificado."""
        from src.core.nodos import NodoTablero
        
        nodo_tablero = NodoTablero(estado)
        tiempo_inicio = time.time()
        nodo_final, nodos_expandidos, profundidad_maxima = func(nodo_tablero)
        tiempo_final = time.time()

        if nodo_final is not None:
            camino_al_objetivo = nodo_final.acciones()
        else:
            camino_al_objetivo = []

        tiempo_transcurrido = tiempo_final - tiempo_inicio
        return camino_al_objetivo, nodos_expandidos, profundidad_maxima, tiempo_transcurrido

    @staticmethod
    def dibujar(estado):
        """Retorna una representación visual del estado en formato de texto."""
        return '{} {} {}\n{} {} {}\n{} {} {}'.format(*estado)


# Namedtuple para almacenar un algoritmo con su nombre y función
Algorithm = namedtuple('Algorithm', ['name', 'func'])

