"""
Módulo de lógica del juego 8-Puzzle

Este módulo contiene:
- Clase Tablero: Operaciones del tablero y utilidades
- Clase Nodo: Representación base de un nodo en el árbol de búsqueda
- Clase NodoTablero: Nodo específico para el juego 8-Puzzle
- Función a_estrella: Algoritmo de búsqueda A* (A-Estrella)
- Función bfs: Algoritmo de búsqueda en anchura (Breadth-First Search)
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import time
import random
import heapq
from collections import namedtuple, deque

# ==============================================================================
# DEFINICIONES DE TIPOS
# ==============================================================================

# Namedtuple para almacenar un algoritmo con su nombre y función
# Se usa para crear la lista de algoritmos disponibles en la GUI
Algorithm = namedtuple('Algoritmo', ['name', 'func'])

# ==============================================================================
# CLASE TABLERO - Operaciones y utilidades del tablero
# ==============================================================================

class Tablero:
    """
    Clase estática que contiene todas las operaciones relacionadas con el tablero.
    No necesita ser instanciada, todos sus métodos son estáticos.
    """

    # --------------------------------------------------------------------------
    # Métodos de coordenadas
    # --------------------------------------------------------------------------

    @staticmethod
    def traducir_a_2d(indice):
        """
        Convierte un índice 1D (0-8) a coordenadas 2D (fila, columna).
        Args:
            indice: Entero entre 0 y 8 representando la posición en el tablero
        Returns:
            Tupla (fila, columna) con las coordenadas 2D
        Ejemplo:
            indice 0 -> (0, 0)  (esquina superior izquierda)
            indice 4 -> (1, 1)  (centro)
            indice 8 -> (2, 2)  (esquina inferior derecha)
        """
        return indice // 3, indice % 3

    # --------------------------------------------------------------------------
    # Métodos de heurística
    # --------------------------------------------------------------------------

    @staticmethod
    def distancia_manhattan(x1, y1, x2, y2):
        """
        Calcula la distancia Manhattan entre dos puntos.
        La distancia Manhattan es la suma de las diferencias absolutas
        de sus coordenadas cartesianas.
        Args:
            x1, y1: Coordenadas del primer punto
            x2, y2: Coordenadas del segundo punto
        Returns:
            Distancia Manhattan (entero)
        Ejemplo:
            punto A(0,0) a punto B(2,1) -> |0-2| + |0-1| = 2 + 1 = 3
        """
        return abs(x1 - x2) + abs(y1 - y2)

    # --------------------------------------------------------------------------
    # Métodos de movimiento
    # --------------------------------------------------------------------------

    @staticmethod
    def acciones_validas(estado):
        """
        Genera las acciones válidas que se pueden realizar desde un estado.
        El espacio en blanco (0) se puede mover:
        - Arriba (U): si no está en la primera fila
        - Abajo (D): si no está en la última fila
        - Izquierda (L): si no está en la primera columna
        - Derecha (R): si no está en la última columna
        Args:
            estado: Tupla de 9 elementos representando el tablero
        Yields:
            Acciones válidas: 'U', 'D', 'L', 'R'
        """
        indice_vacio = estado.index(0)
        if indice_vacio > 2:
            yield 'U'  # Arriba
        if indice_vacio < 6:
            yield 'D'  # Abajo
        if indice_vacio % 3 > 0:
            yield 'L'  # Izquierda
        if indice_vacio % 3 < 2:
            yield 'R'  # Derecha

    @staticmethod
    def transformar(estado, accion):
        """
        Aplica una acción al estado actual y retorna un nuevo estado.
        Args:
            estado: Tupla de 9 elementos con el estado actual
            accion: Acción a realizar ('U', 'D', 'L', 'R')
        Returns:
            Nueva tupla con el estado transformado
        Nota:
            Se crea una copia del estado para no modificar el original
            (inmutabilidad de las tuplas)
        """
        estado = [*estado]
        indice_vacio = estado.index(0)

        match accion:
            case 'U':  # Mover hacia arriba (intercambiar con la posición de arriba)
                estado[indice_vacio], estado[indice_vacio - 3] = \
                    estado[indice_vacio - 3], estado[indice_vacio]
            case 'D':  # Mover hacia abajo
                estado[indice_vacio], estado[indice_vacio + 3] = \
                    estado[indice_vacio + 3], estado[indice_vacio]
            case 'L':  # Mover hacia la izquierda
                estado[indice_vacio], estado[indice_vacio - 1] = \
                    estado[indice_vacio - 1], estado[indice_vacio]
            case 'R':  # Mover hacia la derecha
                estado[indice_vacio], estado[indice_vacio + 1] = \
                    estado[indice_vacio + 1], estado[indice_vacio]

        return tuple(estado)

    # --------------------------------------------------------------------------
    # Métodos de verificacion de resolubilidad
    # --------------------------------------------------------------------------

    @staticmethod
    def inversiones(estado):
        """
        Cuenta el número de inversiones en el estado.
        Una inversión ocurre cuando un número mayor precede a uno menor
        (ignorando el espacio en blanco que es 0).
        Args:
            estado: Tupla de 9 elementos
        Returns:
            Número total de inversiones (entero)
        Nota:
            Un tablero es resoluble si y solo si el número de inversiones
            es par. Esto se conoce como la "paridad del tablero".
        """
        suma_inversiones = 0
        for i in range(9):
            for j in range(i + 1, 9):
                # Ignoramos el espacio en blanco (0)
                if estado[i] != 0 and estado[j] != 0 and estado[i] > estado[j]:
                    suma_inversiones += 1
        return suma_inversiones

    @staticmethod
    def es_resoluble(estado):
        """
        Verifica si un estado del tablero es resoluble.
        Args:
            estado: Tupla de 9 elementos
        Returns:
            True si el estado es resoluble, False en caso contrario
        Teoría:
            En un tablero de 8-puzzle, un estado es resoluble si y solo si
            el número de inversiones es par.
        """
        return Tablero.inversiones(estado) % 2 == 0

    # --------------------------------------------------------------------------
    # Métodos de generación de estados
    # --------------------------------------------------------------------------

    @staticmethod
    def crear_estado_resoluble():
        """
        Genera un estado aleatorio que es resoluble.
        Returns:
            Tupla de 9 elementos con un estado resoluble aleatorio
        Proceso:
            1. Crear una lista con los números del 0 al 8
            2. Barajar aleatoriamente
            3. Verificar si es resoluble
            4. Si no lo es, repetir el proceso
        """
        estado = [*range(9)]
        while True:
            random.shuffle(estado)
            if Tablero.es_resoluble(estado):
                return tuple(estado)

    # --------------------------------------------------------------------------
    # Métodos de resolución
    # --------------------------------------------------------------------------

    @staticmethod
    def resolver(estado, func):
        """
        Resuelve un estado usando el algoritmo de búsqueda especificado.
        Args:
            estado: Tupla de 9 elementos con el estado inicial
            func: Función del algoritmo de búsqueda (a_estrella o bfs)
        Returns:
            Tupla con:
            - camino_al_objetivo: Lista de acciones para llegar a la solución
            - nodos_expandidos: Número de nodos explorados
            - profundidad_maxima: Profundidad máxima alcanzada en la búsqueda
            - tiempo_transcurrido: Tiempo en segundos que tomó la búsqueda
        """
        # Crear el nodo inicial del tablero
        nodo_tablero = NodoTablero(estado)

        # Medir tiempo de ejecución
        tiempo_inicio = time.time()

        # Ejecutar el algoritmo de búsqueda
        # func puede ser a_estrella o bfs
        nodo_final, nodos_expandidos, profundidad_maxima = func(nodo_tablero)
        tiempo_final = time.time()

        # Obtener el camino de acciones desde el nodo inicial hasta el final
        camino_al_objetivo = nodo_final.acciones()

        # Calcular tiempo total
        tiempo_transcurrido = tiempo_final - tiempo_inicio
        return camino_al_objetivo, nodos_expandidos, profundidad_maxima, tiempo_transcurrido

    # --------------------------------------------------------------------------
    # Métodos de visualización
    # --------------------------------------------------------------------------

    @staticmethod
    def dibujar(estado):
        """
        Retorna una representación visual del estado en formato de texto.
        Args:
            estado: Tupla de 9 elementos
        Returns:
            String con el tablero formateado en 3x3
        """
        return '{} {} {}\n{} {} {}\n{} {} {}'.format(*estado)


# ==============================================================================
# CLASE NODO - Representación base de un nodo en el árbol de búsqueda
# ==============================================================================

class Nodo:
    """
    Clase base para representar un nodo en el árbol de búsqueda.
    Usada como clase padre para NodoTablero.
    """
    def __init__(self, padre=None, profundidad=0):
        """
        Inicializa un nodo.
        Args:
            padre: Referencia al nodo padre (None si es el nodo raíz)
            profundidad: Profundidad del nodo en el árbol (0 para la raíz)
        """
        self.padre = padre
        self.profundidad = profundidad
        self.nodos = []  # Lista de hijos

    def agregar_nodo(self, nodo):
        """
        Agrega un nodo hijo a la lista de hijos del nodo actual.
        Args:
            nodo: Nodo hijo a agregar
        """
        self.nodos.append(nodo)

    def iterar_ancestros(self):
        """
        Generador que itera sobre todos los ancestros del nodo actual.
        Yields:
            Cada nodo ancestro desde el actual hasta la raíz
        """
        nodo_actual = self
        while nodo_actual:
            yield nodo_actual
            nodo_actual = nodo_actual.padre


# ==============================================================================
# CLASE NODOTABLERO - Nodo específico para el juego 8-Puzzle
# ==============================================================================

class NodoTablero(Nodo):
    """
    Representa un nodo en el árbol de búsqueda del 8-Puzzle.
    Hereda de Nodo y añade funcionalidad específica del juego.
    """
    def __init__(self, estado, accion=None, padre=None, profundidad=0):
        """
        Inicializa un nodo del tablero.
        Args:
            estado: Tupla de 9 elementos con la configuración del tablero
            accion: Acción que se aplicó para llegar a este estado (None para la raíz)
            padre: Nodo padre en el árbol de búsqueda
            profundidad: Profundidad en el árbol (número de movimientos desde el inicio)
        """
        super().__init__(padre, profundidad)
        self.estado = estado
        self.accion = accion
        self.objetivo = tuple(range(9))  # Estado objetivo: (0,1,2,3,4,5,6,7,8)
        self.funcion_heuristica = Tablero.distancia_manhattan

    def costo(self):
        """
        Calcula el costo total del nodo (usado por A*).
        El costo total es la suma de:
        - g(n): Profundidad del nodo (costo del camino)
        - h(n): Costo heurístico (distancia Manhattan al objetivo)
        Returns:
            Costo total (entero)
        Fórmula:
            f(n) = g(n) + h(n)
        """
        suma_heuristica = 0

        # Para cada número en el tablero, calcular su distancia al objetivo
        for indice, elemento in enumerate(self.estado):
            # Obtener coordenadas actuales
            x_actual, y_actual = Tablero.traducir_a_2d(indice)

            # Obtener coordenadas objetivo del elemento
            x_objetivo, y_objetivo = Tablero.traducir_a_2d(self.objetivo.index(elemento))

            # Sumar la distancia Manhattan
            suma_heuristica += self.funcion_heuristica(
                x_actual, y_actual,
                x_objetivo, y_objetivo
            )

        # Costo total = heurística + profundidad
        return suma_heuristica + self.profundidad

    def heuristica_sola(self):
        """
        Calcula SOLO el costo heurístico del nodo (usado por avara/Greedy).
        A diferencia de A*, aquí solo se considera la heurística h(n)
        sin importar la profundidad del nodo.
        Returns:
            Costo heurístico (entero) - solo la distancia Manhattan
        Nota:
            Este método es usado por el algoritmo avara (Greedy Best-First Search)
            que solo considera qué tan cerca está el estado del objetivo,
            sin importar cuántos movimientos se han hecho.
        """
        suma_heuristica = 0

        # Para cada número en el tablero, calcular su distancia al objetivo
        for indice, elemento in enumerate(self.estado):
            # Obtener coordenadas actuales
            x_actual, y_actual = Tablero.traducir_a_2d(indice)

            # Obtener coordenadas objetivo del elemento
            x_objetivo, y_objetivo = Tablero.traducir_a_2d(self.objetivo.index(elemento))

            # Sumar la distancia Manhattan
            suma_heuristica += self.funcion_heuristica(
                x_actual, y_actual,
                x_objetivo, y_objetivo
            )

        # Solo la heurística, sin profundidad
        return suma_heuristica

    def expandir(self):
        """
        Expande el nodo generando todos los nodos hijos posibles.
        Cada hijo representa un movimiento válido desde el estado actual.
        Solo se expande si no se ha expandido antes (lazy expansion).
        """
        if not self.nodos:  # Solo expandir si no tiene hijos aún
            # Para cada acción válida, crear un nuevo nodo hijo
            for accion in Tablero.acciones_validas(self.estado):
                # Transformar el estado aplicando la acción
                nuevo_estado = Tablero.transformar(self.estado, accion)

                # Crear el nodo hijo
                self.agregar_nodo(NodoTablero(
                    nuevo_estado,
                    accion=accion,
                    padre=self,
                    profundidad=self.profundidad + 1
                ))

    def acciones(self):
        """
        Retorna la secuencia de acciones desde la raíz hasta este nodo.
        Returns:
            Tupla de acciones ('U', 'D', 'L', 'R') que llevan al estado actual
        """
        # Obtener la acción de cada ancestro (excluyendo la raíz que tiene accion=None)
        return tuple(nodo.accion for nodo in self.iterar_ancestros())[-2::-1]

    def es_objetivo(self):
        """
        Verifica si el estado actual es el estado objetivo.
        Returns:
            True si el estado actual iguala al estado objetivo
        """
        return self.estado == self.objetivo

    # --------------------------------------------------------------------------
    # Métodos de comparación (para Priority Queue en A*)
    # --------------------------------------------------------------------------

    def __lt__(self, otro):
        """Compara nodos por su costo total (para heapq)"""
        return self.costo() < otro.costo()

    def __eq__(self, otro):
        """Compara nodos por igualdad de costo total"""
        return self.costo() == otro.costo()

    # --------------------------------------------------------------------------
    # Métodos de comparación para avara (Greedy)
    # --------------------------------------------------------------------------

    def __lt_avara__(self, otro):
        """
        Compara nodos solo por su heurística (para avara/Greedy).
        Este método es usado por el algoritmo avara que solo considera
        la heurística sin importar la profundidad.
        """
        return self.heuristica_sola() < otro.heuristica_sola()

    def __eq_avara__(self, otro):
        """Compara nodos por igualdad de heurística"""
        return self.heuristica_sola() == otro.heuristica_sola()

    # --------------------------------------------------------------------------
    # Métodos de representación
    # --------------------------------------------------------------------------
    def __str__(self):
        """Representación en string del estado"""
        return Tablero.dibujar(self.estado)

    def __repr__(self):
        """Representación técnica del nodo"""
        return f'Tablero(estado={self.estado}, accion={self.accion}, profundidad={self.profundidad})'

# ==============================================================================
# ALGORITMO A* (A-Estrella)
# ==============================================================================

def a_estrella(nodo_inicial):
    """
    Algoritmo de búsqueda A* (A-Estrella).
    A* es un algoritmo de búsqueda informada que usa una función heurística
    para guiar la búsqueda hacia el objetivo. Es completo y óptimo cuando
    la heurística es admisible.
    Args:
        nodo_inicial: NodoTablero con el estado inicial
    Returns:
        Tupla con:
        - nodo_final: Nodo objetivo encontrado (o None si no hay solución)
        - nodos_expandidos: Cantidad de nodos expandidos
        - profundidad_maxima: Profundidad máxima alcanzada
    Funcionamiento:
        1. Usar una priority queue (heap) ordenada por el costo f(n) = g(n) + h(n)
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
    return None


# ==============================================================================
# ALGORITMO bfs (Breadth-First Search - Búsqueda en Anchura)
# ==============================================================================

def bfs(nodo_inicial):
    """
    Algoritmo de búsqueda en anchura (bfs).
    bfs explora uniformemente todos los nodos al mismo nivel de profundidad
    antes de pasar al siguiente nivel. Garantiza encontrar la solución óptima
    en términos de número de movimientos, pero puede ser muy lento.
    Args:
        nodo_inicial: NodoTablero con el estado inicial
    Returns:
        Tupla con:
        - nodo_final: Nodo objetivo encontrado (o None si no hay solución)
        - nodos_expandidos: Cantidad de nodos expandidos
        - profundidad_maxima: Profundidad máxima alcanzada
    Funcionamiento:
        1. Usar una cola (FIFO) para la frontera
        2. Siempre expandir el nodo más antiguo en la frontera
        3. Mantener un conjunto de estados explorados
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
        # Sacra el nodo más antiguo de la frontera
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
    return None


# ==============================================================================
# ALGORITMO avara (Greedy Best-First Search - Búsqueda Voraz)
# ==============================================================================

def avara(nodo_inicial):
    """
    Algoritmo de búsqueda avara (Greedy Best-First Search).
    avara es un algoritmo de búsqueda informada que solo considera
    la heurística h(n) para guiar la búsqueda, SIN tener en cuenta
    el costo del camino g(n).
    Es muy rápido pero NO garantiza encontrar la solución óptima.
    Puede encontrar soluciones subóptimas (más movimientos de lo necesario).
    Args:
        nodo_inicial: NodoTablero con el estado inicial
    Returns:
        Tupla con:
        - nodo_final: Nodo objetivo encontrado (o None si no hay solución)
        - nodos_expandidos: Cantidad de nodos expandidos
        - profundidad_maxima: Profundidad máxima alcanzada
    Funcionamiento:
        1. Usar una priority queue (heap) ordenada solo por heurística h(n)
        2. Siempre expandir el nodo que parezca más cercano al objetivo
        3. NO considera cuántos movimientos se han hecho (g(n))
    Diferencia con A*:
        - A*: f(n) = g(n) + h(n)  -> Garantiza solución óptima
        - avara: f(n) = h(n)       -> Rápido pero puede no ser óptimo
    Ejemplo:
        Si un estado tiene distancia Manhattan 5 pero está a profundidad 20,
        avara lo elegirá antes que uno con distancia 6 a profundidad 2.
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
    return None


# ==============================================================================
# CÓDIGO DE PRUEBA (se ejecuta cuando se ejecuta utils.py directamente)
# ==============================================================================

if __name__ == '__main__':
    # --------------------------------------------------------------------------
    # Prueba de los algoritmos
    # --------------------------------------------------------------------------

    print("=" * 60)
    print("PRUEBA DEL JUEGO 8-PUZZLE")
    print("=" * 60)

    # Crear un estado inicial aleatorio resoluble
    print("\n[1] Generando estado inicial aleatorio...")
    estado_inicial = Tablero.crear_estado_resoluble()
    print("Estado inicial:")
    print(Tablero.dibujar(estado_inicial))

    # --------------------------------------------------------------------------
    # Resolver con A*
    # --------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("[2] Resolviendo con algoritmo A*")
    print("=" * 60)

    camino_al_objetivo, nodos_expandidos, profundidad_maxima, tiempo = \
        Tablero.resolver(estado_inicial, a_estrella)

    print("\nResultados:")
    print(f"  - Tiempo: {round(tiempo, 4)} segundos")
    print(f"  - Movimientos: {len(camino_al_objetivo)}")
    print(f"  - Nodos expandidos: {nodos_expandidos}")
    print(f"  - Profundidad máxima: {profundidad_maxima}")
    print(f"  - Secuencia de acciones: {camino_al_objetivo}")

    # --------------------------------------------------------------------------
    # Resolver con bfs
    # --------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("[3] Resolviendo con algoritmo bfs")
    print("=" * 60)

    camino_al_objetivo, nodos_expandidos, profundidad_maxima, tiempo = \
        Tablero.resolver(estado_inicial, bfs)

    print("\nResultados:")
    print(f"  - Tiempo: {round(tiempo, 4)} segundos")
    print(f"  - Movimientos: {len(camino_al_objetivo)}")
    print(f"  - Nodos expandidos: {nodos_expandidos}")
    print(f"  - Profundidad máxima: {profundidad_maxima}")
    print(f"  - Secuencia de acciones: {camino_al_objetivo}")

    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)
