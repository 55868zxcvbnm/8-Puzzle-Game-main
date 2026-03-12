"""
Módulo de la Interfaz Gráfica del Juego 8-Puzzle

Este módulo actúa como un puente de compatibilidad.
Toda la lógica de la GUI ha sido movida al paquete src/gui/

Para usar la aplicación, importa directamente desde src.gui:
    from src.gui import OchoRompecabezas
"""

# Re-exportar las clases principales para compatibilidad hacia atrás
from src.gui import OchoRompecabezas, PaginaRompecabezas

__all__ = ['OchoRompecabezas', 'PaginaRompecabezas']

