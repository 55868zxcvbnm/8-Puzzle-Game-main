"""
Módulo de la Ventana Principal

Este módulo contiene:
- Clase OchoRompecabezas: Ventana principal de la aplicación

La clase maneja:
- Configuración de la ventana (título, tamaño, icono)
- Contenedor principal para las páginas
- Navegación entre páginas
"""

import os
import tkinter as tk

from src.config import PROPIEDADES_FRAME_BASICO
from src.gui.game_page import PaginaRompecabezas


class OchoRompecabezas(tk.Tk):
    """
    Clase principal de la aplicación.
    Hereda de tk.Tk y representa la ventana principal del juego.
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
        self.geometry('1300x850')  # Tamaño de la ventana
        self.resizable(True, True)  # Ventana redimensionable

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

        # Posicionar la página en el contenedor usando grid
        frame.grid(row=0, column=0, sticky='nsew')

        # Traer la página al frente
        frame.tkraise()

