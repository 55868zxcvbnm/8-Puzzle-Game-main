"""
Módulo de Clases Nodo

Este módulo contiene las clases Nodo y NodoTablero utilizadas
en los algoritmos de búsqueda.
"""

from src.core.tablero import Tablero
from src.core.heuristica import distancia_manhattan


class Nodo:
    """Clase base para representar un nodo en el árbol de búsqueda."""
    
    def __init__(self, padre=None, profundidad=0):
        self.padre = padre
        self.profundidad = profundidad
        self.nodos = []

    def agregar_nodo(self, nodo):
        """Agrega un nodo hijo a la lista de hijos."""
        self.nodos.append(nodo)

    def iterar_ancestros(self):
        """Itera sobre todos los ancestros del nodo actual."""
        nodo_actual = self
        while nodo_actual:
            yield nodo_actual
            nodo_actual = nodo_actual.padre


class NodoTablero(Nodo):
    """Representa un nodo en el árbol de búsqueda del 8-Puzzle."""
    
    def __init__(self, estado, objetivo=None, accion=None, padre=None, profundidad=0):
        super().__init__(padre, profundidad)
        self.estado = estado
        self.accion = accion
        if objetivo is None:
            objetivo = Tablero.ESTADO_OBJETIVO
        self.objetivo = objetivo
        self.funcion_heuristica = distancia_manhattan

    def costo(self):
        """Calcula el costo total del nodo (g(n) + h(n))."""
        suma_heuristica = 0
        for indice, elemento in enumerate(self.estado):
            x_actual, y_actual = Tablero.traducir_a_2d(indice)
            x_objetivo, y_objetivo = Tablero.traducir_a_2d(self.objetivo.index(elemento))
            suma_heuristica += self.funcion_heuristica(x_actual, y_actual, x_objetivo, y_objetivo)
        return suma_heuristica + self.profundidad

    def heuristica_sola(self):
        """Calcula solo el costo heurístico (h(n))."""
        suma_heuristica = 0
        for indice, elemento in enumerate(self.estado):
            x_actual, y_actual = Tablero.traducir_a_2d(indice)
            x_objetivo, y_objetivo = Tablero.traducir_a_2d(self.objetivo.index(elemento))
            suma_heuristica += self.funcion_heuristica(x_actual, y_actual, x_objetivo, y_objetivo)
        return suma_heuristica

    def costo_desde_inicio(self):
        """Retorna g(n) - el costo desde el nodo inicial (profundidad)."""
        return self.profundidad

    def expandir(self):
        """Expande el nodo generando todos los nodos hijos posibles."""
        if not self.nodos:
            for accion in Tablero.acciones_validas(self.estado):
                nuevo_estado = Tablero.transformar(self.estado, accion)
                self.agregar_nodo(NodoTablero(
                    nuevo_estado,
                    objetivo=self.objetivo,
                    accion=accion,
                    padre=self,
                    profundidad=self.profundidad + 1
                ))

    def acciones(self):
        """Retorna la secuencia de acciones desde la raíz hasta este nodo."""
        return tuple(nodo.accion for nodo in self.iterar_ancestros())[-2::-1]

    def es_objetivo(self):
        """Verifica si el estado actual es el estado objetivo."""
        return self.estado == self.objetivo

    def __lt__(self, otro):
        """Compara nodos por su costo total."""
        return self.costo() < otro.costo()

    def __eq__(self, otro):
        """Compara nodos por igualdad de costo total."""
        return self.costo() == otro.costo()

    def __str__(self):
        return Tablero.dibujar(self.estado)

    def __repr__(self):
        return f'NodoTablero(estado={self.estado}, accion={self.accion}, profundidad={self.profundidad})'

