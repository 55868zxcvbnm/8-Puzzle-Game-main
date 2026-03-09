# pylint: disable=redefined-outer-name, attribute-defined-outside-init, unnecessary-lambda
# cSpell:ignore tablero
"""
Módulo de la Interfaz Gráfica del Juego 8-Puzzle

Este módulo contiene:
- Clase OchoRompecabezas: Ventana principal de la aplicación
- Clase PaginaRompecabezas: Página del juego con toda la lógica de la GUI

La interfaz permite al usuario:
- Jugar manualmente haciendo clic en las losetas
- Resolver automáticamente usando A* o bfs
- Mezclar el tablero
- Cambiar entre algoritmos
- Ver el contador de movimientos
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import os          # Para operaciones del sistema de archivos
import tkinter as tk  # Biblioteca principal de GUI
import time       # Para delays en animaciones
from tkinter import ttk  # Widgets adicionales de Tkinter
from PIL import Image, ImageTk  # Procesamiento de imágenes
from threading import Thread  # Hilos para no bloquear la UI

# ==============================================================================
# IMPORTS DE MÓDULOS DEL PROYECTO
# ==============================================================================

from src.config import (
    # Estilos del marco base
    PROPIEDADES_FRAME_BASICO,
    # Estilos de etiquetas
    PROPIEDADES_ETIQUETA_ENCABEZADO,
    PROPIEDADES_ETIQUETA_SUBENCABEZADO,
    PROPIEDADES_ETIQUETA_TEXTO,
    # Estilos de botones
    PROPIEDADES_BOTON_PRIMARIO,
    PROPIEDADES_BOTON_SECUNDARIO,
    PROPIEDADES_BOTON_TERCIARIO,
    PROPIEDADES_BOTON_LOSA
)

# Imports del módulo de lógica del juego
# Algorithm: namedtuple para almacenar algoritmos
# Tablero: Clase con utilidades del tablero
# a_estrella: Algoritmo de búsqueda A* (óptimo)
# avara: Algoritmo de búsqueda avara/Greedy (rápido)
# bfs: Algoritmo de búsqueda en anchura
from src.utils import Algorithm, Tablero, a_estrella, avara, bfs


# ==============================================================================
# CLASE OCHOROMPECABEZAS - Ventana Principal
# ==============================================================================

class OchoRompecabezas(tk.Tk):
    """
    Clase principal de la aplicación.
    hereda de tk.Tk y representa la ventana principal del juego.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicializa la ventana principal de la aplicación.
        Configura el título, tamaño, icono y el contenedor principal.
        """
        # Llamar al constructor de la clase padre
        tk.Tk.__init__(self, *args, **kwargs)

        # Configuración de la ventana
        self.title('Juego del 8-Puzzle')  # Título de la ventana
        self.geometry('750x750')  # Tamaño de la ventana
        self.resizable(False, False)  # Ventana no redimensionable

        # Establecer el icono de la aplicación
        self.iconbitmap('src/assets/images/app.ico')

        # Configurar el protocolo de cierre de ventana
        # Cuando el usuario cierra la ventana, salir completamente
        self.protocol('WM_DELETE_WINDOW', lambda: os._exit(0))

        # --------------------------------------------------------------------------
        # Contenedor Principal
        # --------------------------------------------------------------------------
        # Crear un frame contenedor que ocupará toda la ventana
        self.contenedor = tk.Frame(self)
        self.contenedor.pack(side='top', fill='both', expand=True)

        # Configurar el sistema de geometría grid para el contenedor
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        # Mostrar la página del rompecabezas
        self.mostrar_frame(PaginaRompecabezas, **PROPIEDADES_FRAME_BASICO)

    def mostrar_frame(self, pagina, *args, **kwargs):
        """
        Muestra una página en el contenedor.
        Args:
            pagina: Clase de la página a mostrar
            *args, **kwargs: Argumentos para pasar a la página
        """
        # Crear una instancia de la página
        frame = pagina(self.contenedor, self, *args, **kwargs)

        # Posicion la página en el contenedor usando grid
        frame.grid(row=0, column=0, sticky='nsew')

        # Traer la página al frente
        frame.tkraise()


# ==============================================================================
# CLASE PAGINAROMPECABEZAS - Página del Juego
# ==============================================================================

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
        self.parent = parent  # Widget padre
        self.controller = controller  # Ventana principal

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
        # Lista de algoritmos disponibles para resolver el tablero
        # Se usa namedtuple para almacenar el nombre y la función
        self.algoritmos_disponibles = [
            Algorithm('A*', a_estrella),  # Algoritmo A* (óptimo, usa g(n) + h(n))
            Algorithm('avara', avara),     # Algoritmo avara/Greedy (rápido, solo h(n))
            Algorithm('bfs', bfs)          # bfs (búsqueda sin heurística)
        ]

        # Índice del algoritmo actualmente seleccionado
        self.indice_algoritmo = 0

        # Algoritmo actual (inicialmente A*)
        self.algoritmo = self.algoritmos_disponibles[0]

        # --------------------------------------------------------------------------
        # Estados del Tablero
        # --------------------------------------------------------------------------

        # Estado actual del tablero (tupla de 9 elementos)
        self.estado_tablero_actual = tuple(range(9))

        # Estado objetivo: (0,1,2,3,4,5,6,7,8)
        self.estado_tablero_objetivo = tuple(range(9))

        # Estado guardado (para la función reiniciar)
        self.estado_tablero_guardado = tuple(range(9))

        # --------------------------------------------------------------------------
        # Cargar Imágenes de las Losetas
        # --------------------------------------------------------------------------
        # Cargar las 9 imágenes de las losetas (tile_0.png a tile_8.png)
        # Se carga al inicio para evitar retardos durante el juego
        self.imagenes_losas = [
            ImageTk.PhotoImage(Image.open(f'src/assets/images/tile_{n}.png'))
            for n in range(9)
        ]

        # --------------------------------------------------------------------------
        # Banderas de Estado
        # --------------------------------------------------------------------------

        # Indica si el usuario solicitó detener la resolución
        self.esta_detenido = False

        # Indica si el algoritmo está buscando una solución
        self.esta_resolviendo = False

        # Indica si el juego ha sido completado
        self.esta_completo = False

        # --------------------------------------------------------------------------
        # Inicializar la Interfaz
        # --------------------------------------------------------------------------

        # Crear todos los widgets de la interfaz
        self.mostrar_widgets()

    # ==========================================================================
    # MÉTODOS DE CREACIÓN DE WIDGETS
    # ==========================================================================

    def mostrar_widgets(self):
        """
        Crea y posiciona todos los widgets de la interfaz gráfica.
        widgets creados:
        - Título y subtítulo
        - Marco del rompecabezas (3x3)
        - Botones de control
        - Etiquetas de estado y movimientos
        """

        # --------------------------------------------------------------------------
        # Sección de Título
        # --------------------------------------------------------------------------
        self.frame_titulo = tk.Frame(self, **PROPIEDADES_FRAME_BASICO)
        self.frame_titulo.pack(pady=25)

        # Etiqueta principal con el nombre del juego
        self.etiqueta_encabezado = tk.Label(
            self.frame_titulo,
            text='Juego del 8-Puzzle',
            **PROPIEDADES_ETIQUETA_ENCABEZADO
        )
        self.etiqueta_encabezado.pack()

        # Etiqueta secundario mostrando el algoritmo actual
        self.etiqueta_subencabezado = tk.Label(
            self.frame_titulo,
            text=f'resuelto usando el algoritmo {self.algoritmo.name}',
            **PROPIEDADES_ETIQUETA_SUBENCABEZADO
        )
        self.etiqueta_subencabezado.pack()

        # --------------------------------------------------------------------------
        # Sección del Rompecabezas
        # --------------------------------------------------------------------------
        self.frame_rompecabezas = tk.Frame(self, **PROPIEDADES_FRAME_BASICO)
        self.frame_rompecabezas.pack(padx=10, pady=10)

        # --------------------------------------------------------------------------
        # Sección de Botones de Control
        # --------------------------------------------------------------------------
        self.frame_botones = tk.Frame(self, **PROPIEDADES_FRAME_BASICO)
        self.frame_botones.pack(pady=20)

        # Botón RESOLVER: Inicia la resolución automática
        # Usa el algoritmo seleccionado actualmente (A* o bfs)
        self.boton_resolver = tk.Button(
            self.frame_botones,
            text='resolver',
            command=lambda: self.resolver_tablero(),
            **PROPIEDADES_BOTON_PRIMARIO
        )
        self.boton_resolver.grid(row=0, column=0, padx=10, pady=10)

        # Botón REINICIAR: Reinicia al último estado barajado
        self.boton_reiniciar = tk.Button(
            self.frame_botones,
            text='reiniciar',
            command=lambda: self.reiniciar_tablero(),
            **PROPIEDADES_BOTON_SECUNDARIO
        )
        self.boton_reiniciar.grid(row=0, column=1, padx=10, pady=10)

        # Botón MEZCLAR: Baraja el tablero con un nuevo estado
        self.boton_mezclar = tk.Button(
            self.frame_botones,
            text='mezclar',
            command=lambda: self.mezclar_tablero(),
            **PROPIEDADES_BOTON_PRIMARIO
        )
        self.boton_mezclar.grid(row=0, column=2, padx=10, pady=10)

        # Botón CAMBIAR: Alterna entre A* y bfs
        self.boton_cambiar = tk.Button(
            self.frame_botones,
            text='cambiar',
            command=lambda: self.cambiar_algoritmo(),
            **PROPIEDADES_BOTON_TERCIARIO
        )
        self.boton_cambiar.grid(row=0, column=3, padx=10, pady=10)

        # --------------------------------------------------------------------------
        # Etiquetas de Estado y Movimientos
        # --------------------------------------------------------------------------

        # Muestra el número de movimientos realizados
        self.etiqueta_movimientos = tk.Label(
            self.frame_rompecabezas,
            text=f'Movimientos: {self.movimientos}',
            **PROPIEDADES_ETIQUETA_TEXTO
        )
        self.etiqueta_movimientos.grid(row=0, column=0, sticky='w', padx=10, pady=5)

        # Muestra el estado actual del juego
        self.etiqueta_estado = tk.Label(
            self.frame_rompecabezas,
            text='Jugando...',
            **PROPIEDADES_ETIQUETA_TEXTO
        )
        self.etiqueta_estado.grid(row=0, column=1, sticky='e', padx=10, pady=5)

        # Separado visual entre las etiquetas y el tablero
        self.separador = ttk.Separator(self.frame_rompecabezas, orient='horizontal')
        self.separador.grid(row=1, columnspan=2, sticky='ew', pady=10)

        # --------------------------------------------------------------------------
        # Marco del Tablero (3x3)
        # --------------------------------------------------------------------------

        # Frame que contiene los 9 botones del tablero
        self.frame_tablero = tk.Frame(self.frame_rompecabezas, **PROPIEDADES_FRAME_BASICO)
        self.frame_tablero.grid(row=2, columnspan=2)

        # Inicializar los botones del tablero
        self.inicializar_tablero()

        # Barajar el tablero al inicio
        self.mezclar_tablero()

        # --------------------------------------------------------------------------
        # Configurar Controles de Teclado
        # --------------------------------------------------------------------------
        # Bind de teclas de flecha para mover las losetas

        # Flecha arriba -> Mover loseta hacia ABAJO (espacio vacío sube)
        self.controller.bind('<Up>', lambda event: self.transformar_teclas('D'))

        # Flecha abajo -> Mover loseta hacia ARRIBA
        self.controller.bind('<Down>', lambda event: self.transformar_teclas('U'))

        # Flecha izquierda -> Mover loseta hacia DERECHA
        self.controller.bind('<Left>', lambda event: self.transformar_teclas('R'))

        # Flecha derecha -> Mover loseta hacia IZQUIERDA
        self.controller.bind('<Right>', lambda event: self.transformar_teclas('L'))

    def inicializar_tablero(self):
        """
        Crea los 9 botones que forman el tablero del juego.
        Cada botón representa una posición en el tablero 3x3.
        Se posiciona usando grid (fila, columna).
        """
        for indice in range(9):
            # Crear un botón para cada posición del tablero
            self.tablero.append(
                tk.Button(self.frame_tablero, **PROPIEDADES_BOTON_LOSA)
            )

            # Posicionar en la grilla 3x3
            # Fila = indice // 3 (división entera)
            # Columna = indice % 3 (resto)
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
        """
        Actualiza la visualización del tablero con un nuevo estado.
        Args:
            estado: Tupla de 9 elementos con el nuevo estado
            tiempo_retardo: Delay opcional para animaciones
        """
        # Para cada posición en el estado
        for indice_losa, valor_losa in enumerate(estado):
            # Configurar la imagen y texto del botón
            self.tablero[indice_losa].configure(
                image=self.imagenes_losas[valor_losa],
                text=valor_losa,
                state='normal',
                # Usar lambda con argumento por defecto para capturar el valor correcto
                command=lambda indice_losa=indice_losa: self.transformar_clic(indice_losa)
            )

            # Deshabilitado el botón si es el espacio en blanco (0)
            if valor_losa == 0:
                self.tablero[indice_losa].configure(state='disabled')

        # Actualizar el estado interno
        self.estado_tablero_actual = estado

        # Delay opcional para animaciones
        if tiempo_retardo > 0:
            time.sleep(tiempo_retardo)

    # ==========================================================================
    # MÉTODOS DE RESOLUCIÓN AUTOMÁTICA
    # ==========================================================================

    def resolver_tablero(self):
        """
        Inicia la resolución automática del tablero.
        Crea un hilo separado para ejecutar el algoritmo de búsqueda
        sin bloquear la interfaz gráfica.
        Nota:
            Se usa un hilo (Thread) para que la UI saga respondiendo
            mientras el algoritmo busca la solución.
        """
        # Solo iniciar si no hay otra resolución en progreso
        if not self.esta_resolviendo:
            # Reiniciar el tablero antes de resolver
            self.reiniciar_tablero()

            # Crear un hilo para ejecutar la solución
            # target especifica la función a ejecutar en el hilo
            self.hilo_solucion = Thread(target=self.ejecutar_solucion)

            # Iniciar el hilo
            self.hilo_solucion.start()

    def ejecutar_solucion(self):
        """
        Ejecuta el algoritmo de búsqueda en un hilo separado.

        Esta función:
        1. Llama al algoritmo seleccionado (a_estrella o bfs)
        2. Imprime información de debug en consola
        3. Anima los movimientos uno por uno

        El algoritmo usado se especifica en:
        - self.algoritmo.func -> función (a_estrella o bfs)
        """
        # Resetear banderas de estado
        self.esta_detenido = False
        self.esta_resolviendo = True
        self.esta_completo = False

        # Actualizar etiqueta de estado
        self.actualizar_estado('Resolviendo...')

        # Mensaje de debug
        print('\nBuscando solucion...')

        # --------------------------------------------------------------------------
        # LLAMAR AL ALGORITMO DE BÚSQUEDA
        # --------------------------------------------------------------------------
        # Usamos Tablero.resolver() que acepta:
        # - self.estado_tablero_actual: Estado inicial
        # - self.algoritmo.func: Función del algoritmo (a_estrella o bfs)
        #
        # Retorna:
        # - camino_al_objetivo: Lista de acciones para resolver
        # - nodos_expandidos: Cantidad de nodos explorados
        # - profundidad_maxima: Profundidad máxima alcanzada
        # - tiempo_transcurrido: Tiempo de ejecución
        camino_al_objetivo, nodos_expandidos, profundidad_maxima, tiempo_transcurrido = \
            Tablero.resolver(self.estado_tablero_actual, self.algoritmo.func)

        # Verificar si no fue detenido por el usuario
        if not self.esta_detenido:
            # Imprimir resultados
            print(f'Completado en {round(tiempo_transcurrido, 4)} segundo(s) con {len(camino_al_objetivo)} movimientos usando {self.algoritmo.name}')
            print(f'Tiene una profundidad maxima de busqueda de {profundidad_maxima} y nodos expandidos de {nodos_expandidos}')
            print('Acciones:', *camino_al_objetivo)
        else:
            print('Detenido')

        # --------------------------------------------------------------------------
        # Animar la Solución
        # --------------------------------------------------------------------------

        # Si hay un camino disponible
        if camino_al_objetivo:
            print('\nMoviendo tablero...')
            self.actualizar_estado('Moviendo...')

            # Delay entre cada movimiento para animación
            tiempo_retardo = 0.75
            time.sleep(tiempo_retardo)

            # Ejecutar cada acción del camino
            for accion in camino_al_objetivo:
                # Verificar si el usuario solicitó detener
                if self.esta_detenido:
                    print('Detenido')
                    self.actualizar_estado('Jugando...')
                    break
                else:
                    # Aplicar el movimiento
                    # tiempo_retardo=0.5 para animación fluida
                    self.transformar_estado(accion, tiempo_retardo=0.5)
            else:
                # Si el bucle terminó sin break
                print('Animacion del tablero completada')
                self.actualizar_estado('Resuelto!')
                self.esta_completo = True

            self.esta_resolviendo = False

        else:
            # No se encontró solución
            self.esta_resolviendo = False
            self.actualizar_estado('Jugando...')

    # ==========================================================================
    # MÉTODOS DE CONTROL DEL JUEGO
    # ==========================================================================

    def reiniciar_tablero(self):
        """
        Reinicia el tablero al último estado barajado.
        Guarda el estado actual antes de reiniciar.
        """
        # Detener cualquier solución en progreso
        self.detener_solucion()

        # Resetear contador de movimientos
        self.actualizar_movimientos(0)

        # Actualizar estado
        self.actualizar_estado('Jugando...')

        # Poblar con el estado guardado
        self.poblar_tablero(estado=self.estado_tablero_guardado)

    def mezclar_tablero(self):
        """
        Baraja el tablero generando un nuevo estado aleatorio resoluble.
        Usa Tablero.crear_estado_resoluble() que garantiza
        que el estado generado tiene solución.
        """
        # Generar nuevo estado aleatorio
        self.estado_tablero_guardado = Tablero.crear_estado_resoluble()

        # Reiniciar con el nuevo estado
        self.reiniciar_tablero()

    def detener_solucion(self):
        """
        Detiene una resolución en progreso.
        Establece la bandera esta_detenido para que el hilo
        de resolución se detenga.
        """
        if self.esta_resolviendo and not self.esta_detenido:
            self.esta_detenido = True
        self.esta_completo = False

    def cambiar_algoritmo(self):
        """
        Cambia entre los algoritmos disponibles (A* <-> bfs).
        Itera cíclicamente por la lista de algoritmos.
        """
        # Reiniciar el tablero antes de cambiar
        self.reiniciar_tablero()

        # Mover al siguiente algoritmo (cíclicamente)
        self.indice_algoritmo = (self.indice_algoritmo + 1) % len(self.algoritmos_disponibles)

        # Actualizar algoritmo actual
        self.algoritmo = self.algoritmos_disponibles[self.indice_algoritmo]

        # Actualizar la etiqueta
        self.etiqueta_subencabezado.configure(
            text=f'resuelto usando el algoritmo {self.algoritmo.name}'
        )

    # ==========================================================================
    # MÉTODOS DE INTERACCIÓN DEL JUGADOR
    # ==========================================================================

    def transformar_clic(self, indice_losa):
        """
        Maneja el evento de clic en una loseta.
        Verifica si el movimiento es válido y lo ejecuta.
        Args:
            indice_losa: Índice de la loseta clickeada
        """
        # Obtener acciones válidas desde el estado actual
        acciones_posibles = Tablero.acciones_validas(self.estado_tablero_actual)

        # Obtener índice del espacio vacío
        indice_vacio = self.estado_tablero_actual.index(0)

        # Obtener el valor de la loseta clickeada
        valor_losa = int(self.tablero[indice_losa].cget('text'))

        # Verificar cada acción posible
        for accion in acciones_posibles:
            # Solo procesar si no está resolviendo ni completado
            if not self.esta_resolviendo and not self.esta_completo:
                # Acción ARRIBA: espacio vacío debe estar 3 posiciones arriba
                if accion == 'U' and self.estado_tablero_actual[indice_vacio - 3] == valor_losa:
                    self.transformar_estado(accion)

                # Acción ABAJO
                elif accion == 'D' and self.estado_tablero_actual[indice_vacio + 3] == valor_losa:
                    self.transformar_estado(accion)

                # Acción IZQUIERDA
                elif accion == 'L' and self.estado_tablero_actual[indice_vacio - 1] == valor_losa:
                    self.transformar_estado(accion)

                # Acción DERECHA
                elif accion == 'R' and self.estado_tablero_actual[indice_vacio + 1] == valor_losa:
                    self.transformar_estado(accion)

        # Verificar si se completó el juego
        if not self.esta_completo and self.estado_tablero_actual == self.estado_tablero_objetivo:
            self.actualizar_estado('Bien hecho!')
            self.esta_completo = True

    def transformar_teclas(self, accion):
        """
        Maneja el evento de teclado para mover losetas.
        Args:
            accion: Acción a realizar ('U', 'D', 'L', 'R')
        """
        # Verificar si el movimiento es válido
        if not self.esta_resolviendo and not self.esta_completo:
            if accion in Tablero.acciones_validas(self.estado_tablero_actual):
                self.transformar_estado(accion)

        # Verificar victoria
        if not self.esta_completo and self.estado_tablero_actual == self.estado_tablero_objetivo:
            self.actualizar_estado('Bien hecho!')
            self.esta_completo = True

    def transformar_estado(self, accion, tiempo_retardo=0):
        """
        Aplica una acción al estado actual del tablero.
        Intercambia visualmente las losetas en la interfaz.
        Args:
            accion: Acción a realizar ('U', 'D', 'L', 'R')
            tiempo_retardo: Delay opcional para animaciones
        """
        # --------------------------------------------------------------------------
        # Calcular nuevo estado usando la lógica del módulo utils
        # --------------------------------------------------------------------------
        nuevo_estado = Tablero.transformar(self.estado_tablero_actual, accion)

        # --------------------------------------------------------------------------
        # Intercambiar visualmente las losetas
        # --------------------------------------------------------------------------

        # Obtener índices de las losetas involucradas
        indice_actual = self.estado_tablero_actual.index(0)
        nuevo_indice = nuevo_estado.index(0)

        # Referencias a los botones
        primera_losa = self.tablero[indice_actual]
        segunda_losa = self.tablero[nuevo_indice]

        # Obtener propiedades de ambas losetas
        propiedades_primera_losa = self.obtener_propiedad_losa(primera_losa)
        propiedades_segunda_losa = self.obtener_propiedad_losa(segunda_losa)

        # Intercambiar propiedades (efecto visual de movimiento)
        self.establecer_propiedad_losa(primera_losa, propiedades_segunda_losa)
        self.establecer_propiedad_losa(segunda_losa, propiedades_primera_losa)

        # --------------------------------------------------------------------------
        # Actualizar estado interno
        # --------------------------------------------------------------------------

        self.estado_tablero_actual = nuevo_estado

        # Incrementar contador si no está completado
        if not self.esta_completo:
            self.actualizar_movimientos(self.movimientos + 1)

        # Delay opcional
        if tiempo_retardo > 0:
            time.sleep(tiempo_retardo)

    # ==========================================================================
    # MÉTODOS AUXILIARES
    # ==========================================================================

    def obtener_propiedad_losa(self, losa):
        """
        Obtiene las propiedades de un botón.
        Args:
            losa: Botón del tablero
        Returns:
            Diccionario con las propiedades
        """
        return {
            'text': losa.cget('text'),
            'background': losa.cget('background'),
            'image': losa.cget('image'),
            'state': losa.cget('state')
        }

    def establecer_propiedad_losa(self, losa, propiedades):
        """
        Establece las propiedades de un botón.
        Args:
            losa: Botón del tablero
            propiedades: Diccionario de propiedades
        """
        losa.configure(**propiedades)

    def actualizar_movimientos(self, movimientos):
        """
        Actualiza el contador de movimientos.
        Args:
            movimientos: Nuevo valor del contador
        """
        self.movimientos = movimientos
        self.etiqueta_movimientos.configure(text=f'Movimientos: {self.movimientos}')

    def actualizar_estado(self, estado):
        """
        Actualiza la etiqueta de estado.

        Args:
            estado: Nuevo estado a mostrar
        """
        self.etiqueta_estado.configure(text=estado)
