# pylint: disable=redefined-outer-name, attribute-defined-outside-init, unnecessary-lambda
# cSpell:ignore tablero
"""
Módulo de la Página del Juego

Este módulo contiene:
- Clase PaginaRompecabezas: Página del juego con toda la lógica de la GUI

La interfaz permite al usuario:
- Jugar manualmente haciendo clic en las losetas
- Resolver automáticamente usando A*, avara o BFS
- Mezclar el tablero
- Cambiar entre algoritmos
- Ver el contador de movimientos
"""

import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from threading import Thread

from src.config import (
    PROPIEDADES_FRAME_BASICO,
    PROPIEDADES_ETIQUETA_ENCABEZADO,
    PROPIEDADES_ETIQUETA_SUBENCABEZADO,
    PROPIEDADES_ETIQUETA_TEXTO,
    PROPIEDADES_BOTON_PRIMARIO,
    PROPIEDADES_BOTON_SECUNDARIO,
    PROPIEDADES_BOTON_TERCIARIO,
    PROPIEDADES_BOTON_LOSA
)

from src.utils import Algorithm, Tablero
from src.algorithms import a_estrella, avara, bfs


class PaginaRompecabezas(tk.Frame):
    """
    Clase que representa la página principal del juego.
    Contiene toda la lógica de la interfaz y las interacciones del usuario.
    """

    def __init__(self, parent, controller, *args, **kwargs):
        """
        Inicializa la página del rompecabezas.
        
        Args:
            parent: Widget padre (el contenedor)
            controller: Referencia a la ventana principal (OchoRompecabezas)
        """
        # Llamar al constructor de la clase padre
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Referencias
        self.parent = parent
        self.controller = controller

        # --------------------------------------------------------------------------
        # Variables de Estado del Juego
        # --------------------------------------------------------------------------

        # Contador de movimientos realizados por el jugador
        self.movimientos = 0

        # Lista de botones que representan las 9 posiciones del tablero
        self.tablero = []

        # --------------------------------------------------------------------------
        # Configuración de Algoritmos Disponibles
        # --------------------------------------------------------------------------
        self.algoritmos_disponibles = [
            Algorithm('A*', a_estrella),
            Algorithm('avara', avara),
            Algorithm('bfs', bfs)
        ]

        self.indice_algoritmo = 0
        self.algoritmo = self.algoritmos_disponibles[0]

        # --------------------------------------------------------------------------
        # Estados del Tablero
        # --------------------------------------------------------------------------
        self.estado_tablero_actual = tuple(range(9))
        self.estado_tablero_objetivo = tuple(range(9))
        self.estado_tablero_guardado = tuple(range(9))

        # --------------------------------------------------------------------------
        # Cargar Imágenes de las Losetas
        # --------------------------------------------------------------------------
        self.imagenes_losas = [
            ImageTk.PhotoImage(Image.open(f'src/assets/images/tile_{n}.png'))
            for n in range(9)
        ]

        # --------------------------------------------------------------------------
        # Banderas de Estado
        # --------------------------------------------------------------------------
        self.esta_detenido = False
        self.esta_resolviendo = False
        self.esta_completo = False

        # --------------------------------------------------------------------------
        # Inicializar la Interfaz
        # --------------------------------------------------------------------------
        self.mostrar_widgets()

    # ==========================================================================
    # MÉTODOS DE CREACIÓN DE WIDGETS
    # ==========================================================================

    def mostrar_widgets(self):
        """
        Crea y posiciona todos los widgets de la interfaz gráfica.
        """
        # Sección de Título
        self.frame_titulo = tk.Frame(self, **PROPIEDADES_FRAME_BASICO)
        self.frame_titulo.pack(pady=25)

        self.etiqueta_encabezado = tk.Label(
            self.frame_titulo,
            text='Juego del 8-Puzzle',
            **PROPIEDADES_ETIQUETA_ENCABEZADO
        )
        self.etiqueta_encabezado.pack()

        self.etiqueta_subencabezado = tk.Label(
            self.frame_titulo,
            text=f'resuelto usando el algoritmo {self.algoritmo.name}',
            **PROPIEDADES_ETIQUETA_SUBENCABEZADO
        )
        self.etiqueta_subencabezado.pack()

        # Sección del Rompecabezas
        self.frame_rompecabezas = tk.Frame(self, **PROPIEDADES_FRAME_BASICO)
        self.frame_rompecabezas.pack(padx=10, pady=10)

        # Sección de Botones de Control
        self.frame_botones = tk.Frame(self, **PROPIEDADES_FRAME_BASICO)
        self.frame_botones.pack(pady=20)

        # Botón RESOLVER
        self.boton_resolver = tk.Button(
            self.frame_botones,
            text='resolver',
            command=lambda: self.resolver_tablero(),
            **PROPIEDADES_BOTON_PRIMARIO
        )
        self.boton_resolver.grid(row=0, column=0, padx=10, pady=10)

        # Botón REINICIAR
        self.boton_reiniciar = tk.Button(
            self.frame_botones,
            text='reiniciar',
            command=lambda: self.reiniciar_tablero(),
            **PROPIEDADES_BOTON_SECUNDARIO
        )
        self.boton_reiniciar.grid(row=0, column=1, padx=10, pady=10)

        # Botón MEZCLAR
        self.boton_mezclar = tk.Button(
            self.frame_botones,
            text='mezclar',
            command=lambda: self.mezclar_tablero(),
            **PROPIEDADES_BOTON_PRIMARIO
        )
        self.boton_mezclar.grid(row=0, column=2, padx=10, pady=10)

        # Botón CAMBIAR
        self.boton_cambiar = tk.Button(
            self.frame_botones,
            text='cambiar',
            command=lambda: self.cambiar_algoritmo(),
            **PROPIEDADES_BOTON_TERCIARIO
        )
        self.boton_cambiar.grid(row=0, column=3, padx=10, pady=10)

        # Etiquetas de Estado y Movimientos
        self.etiqueta_movimientos = tk.Label(
            self.frame_rompecabezas,
            text=f'Movimientos: {self.movimientos}',
            **PROPIEDADES_ETIQUETA_TEXTO
        )
        self.etiqueta_movimientos.grid(row=0, column=0, sticky='w', padx=10, pady=5)

        self.etiqueta_estado = tk.Label(
            self.frame_rompecabezas,
            text='Jugando...',
            **PROPIEDADES_ETIQUETA_TEXTO
        )
        self.etiqueta_estado.grid(row=0, column=1, sticky='e', padx=10, pady=5)

        self.separador = ttk.Separator(self.frame_rompecabezas, orient='horizontal')
        self.separador.grid(row=1, columnspan=2, sticky='ew', pady=10)

        # Marco del Tablero (3x3)
        self.frame_tablero = tk.Frame(self.frame_rompecabezas, **PROPIEDADES_FRAME_BASICO)
        self.frame_tablero.grid(row=2, columnspan=2)

        self.inicializar_tablero()
        self.mezclar_tablero()

        # Controles de Teclado
        self.controller.bind('<Up>', lambda event: self.transformar_teclas('D'))
        self.controller.bind('<Down>', lambda event: self.transformar_teclas('U'))
        self.controller.bind('<Left>', lambda event: self.transformar_teclas('R'))
        self.controller.bind('<Right>', lambda event: self.transformar_teclas('L'))

    def inicializar_tablero(self):
        """Crea los 9 botones que forman el tablero del juego."""
        for indice in range(9):
            self.tablero.append(
                tk.Button(self.frame_tablero, **PROPIEDADES_BOTON_LOSA)
            )
            self.tablero[indice].grid(
                row=indice // 3,
                column=indice % 3,
                padx=10,
                pady=10
            )

    # ==========================================================================
    # MÉTODOS DE ACTUALIZACIÓN DEL TABLERO
    # ==========================================================================

    def poblar_tablero(self, estado, tiempo_retardo=0):
        """Actualiza la visualización del tablero con un nuevo estado."""
        for indice_losa, valor_losa in enumerate(estado):
            self.tablero[indice_losa].configure(
                image=self.imagenes_losas[valor_losa],
                text=valor_losa,
                state='normal',
                command=lambda indice_losa=indice_losa: self.transformar_clic(indice_losa)
            )

            if valor_losa == 0:
                self.tablero[indice_losa].configure(state='disabled')

        self.estado_tablero_actual = estado

        if tiempo_retardo > 0:
            time.sleep(tiempo_retardo)

    # ==========================================================================
    # MÉTODOS DE RESOLUCIÓN AUTOMÁTICA
    # ==========================================================================

    def resolver_tablero(self):
        """Inicia la resolución automática del tablero."""
        if not self.esta_resolviendo:
            self.reiniciar_tablero()
            self.hilo_solucion = Thread(target=self.ejecutar_solucion)
            self.hilo_solucion.start()

    def ejecutar_solucion(self):
        """Ejecuta el algoritmo de búsqueda en un hilo separado."""
        self.esta_detenido = False
        self.esta_resolviendo = True
        self.esta_completo = False

        self.actualizar_estado('Resolviendo...')
        print('\nBuscando solucion...')

        camino_al_objetivo, nodos_expandidos, profundidad_maxima, tiempo_transcurrido = \
            Tablero.resolver(self.estado_tablero_actual, self.algoritmo.func)

        if not self.esta_detenido:
            print(f'Completado en {round(tiempo_transcurrido, 4)} segundo(s) con {len(camino_al_objetivo)} movimientos usando {self.algoritmo.name}')
            print(f'Tiene una profundidad maxima de busqueda de {profundidad_maxima} y nodos expandidos de {nodos_expandidos}')
            print('Acciones:', *camino_al_objetivo)
        else:
            print('Detenido')

        # Animar la Solución
        if camino_al_objetivo:
            print('\nMoviendo tablero...')
            self.actualizar_estado('Moviendo...')
            time.sleep(0.75)

            for accion in camino_al_objetivo:
                if self.esta_detenido:
                    print('Detenido')
                    self.actualizar_estado('Jugando...')
                    break
                else:
                    self.transformar_estado(accion, tiempo_retardo=0.5)
            else:
                print('Animacion del tablero completada')
                self.actualizar_estado('Resuelto!')
                self.esta_completo = True

            self.esta_resolviendo = False
        else:
            self.esta_resolviendo = False
            self.actualizar_estado('Jugando...')

    # ==========================================================================
    # MÉTODOS DE CONTROL DEL JUEGO
    # ==========================================================================

    def reiniciar_tablero(self):
        """Reinicia el tablero al último estado barajado."""
        self.detener_solucion()
        self.actualizar_movimientos(0)
        self.actualizar_estado('Jugando...')
        self.poblar_tablero(estado=self.estado_tablero_guardado)

    def mezclar_tablero(self):
        """Baraja el tablero generando un nuevo estado aleatorio resoluble."""
        self.estado_tablero_guardado = Tablero.crear_estado_resoluble()
        self.reiniciar_tablero()

    def detener_solucion(self):
        """Detiene una resolución en progreso."""
        if self.esta_resolviendo and not self.esta_detenido:
            self.esta_detenido = True
        self.esta_completo = False

    def cambiar_algoritmo(self):
        """Cambia entre los algoritmos disponibles."""
        self.reiniciar_tablero()
        self.indice_algoritmo = (self.indice_algoritmo + 1) % len(self.algoritmos_disponibles)
        self.algoritmo = self.algoritmos_disponibles[self.indice_algoritmo]
        self.etiqueta_subencabezado.configure(
            text=f'resuelto usando el algoritmo {self.algoritmo.name}'
        )

    # ==========================================================================
    # MÉTODOS DE INTERACCIÓN DEL JUGADOR
    # ==========================================================================

    def transformar_clic(self, indice_losa):
        """Maneja el evento de clic en una loseta."""
        acciones_posibles = Tablero.acciones_validas(self.estado_tablero_actual)
        indice_vacio = self.estado_tablero_actual.index(0)
        valor_losa = int(self.tablero[indice_losa].cget('text'))

        for accion in acciones_posibles:
            if not self.esta_resolviendo and not self.esta_completo:
                if accion == 'U' and self.estado_tablero_actual[indice_vacio - 3] == valor_losa:
                    self.transformar_estado(accion)
                elif accion == 'D' and self.estado_tablero_actual[indice_vacio + 3] == valor_losa:
                    self.transformar_estado(accion)
                elif accion == 'L' and self.estado_tablero_actual[indice_vacio - 1] == valor_losa:
                    self.transformar_estado(accion)
                elif accion == 'R' and self.estado_tablero_actual[indice_vacio + 1] == valor_losa:
                    self.transformar_estado(accion)

        if not self.esta_completo and self.estado_tablero_actual == self.estado_tablero_objetivo:
            self.actualizar_estado('Bien hecho!')
            self.esta_completo = True

    def transformar_teclas(self, accion):
        """Maneja el evento de teclado para mover losetas."""
        if not self.esta_resolviendo and not self.esta_completo:
            if accion in Tablero.acciones_validas(self.estado_tablero_actual):
                self.transformar_estado(accion)

        if not self.esta_completo and self.estado_tablero_actual == self.estado_tablero_objetivo:
            self.actualizar_estado('Bien hecho!')
            self.esta_completo = True

    def transformar_estado(self, accion, tiempo_retardo=0):
        """Aplica una acción al estado actual del tablero."""
        nuevo_estado = Tablero.transformar(self.estado_tablero_actual, accion)

        indice_actual = self.estado_tablero_actual.index(0)
        nuevo_indice = nuevo_estado.index(0)

        primera_losa = self.tablero[indice_actual]
        segunda_losa = self.tablero[nuevo_indice]

        propiedades_primera_losa = self.obtener_propiedad_losa(primera_losa)
        propiedades_segunda_losa = self.obtener_propiedad_losa(segunda_losa)

        self.establecer_propiedad_losa(primera_losa, propiedades_segunda_losa)
        self.establecer_propiedad_losa(segunda_losa, propiedades_primera_losa)

        self.estado_tablero_actual = nuevo_estado

        if not self.esta_completo:
            self.actualizar_movimientos(self.movimientos + 1)

        if tiempo_retardo > 0:
            time.sleep(tiempo_retardo)

    # ==========================================================================
    # MÉTODOS AUXILIARES
    # ==========================================================================

    def obtener_propiedad_losa(self, losa):
        """Obtiene las propiedades de un botón."""
        return {
            'text': losa.cget('text'),
            'background': losa.cget('background'),
            'image': losa.cget('image'),
            'state': losa.cget('state')
        }

    def establecer_propiedad_losa(self, losa, propiedades):
        """Establece las propiedades de un botón."""
        losa.configure(**propiedades)

    def actualizar_movimientos(self, movimientos):
        """Actualiza el contador de movimientos."""
        self.movimientos = movimientos
        self.etiqueta_movimientos.configure(text=f'Movimientos: {self.movimientos}')

    def actualizar_estado(self, estado):
        """Actualiza la etiqueta de estado."""
        self.etiqueta_estado.configure(text=estado)

