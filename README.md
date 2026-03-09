# Juego del 8-Puzzle

## Descripción General

Este proyecto es una implementación del clásico juego de tablero 8-Puzzle (también conocido como "Juego del 15" en su versión 3x3) desarrollado en Python utilizando la biblioteca **Tkinter** para la interfaz gráfica de usuario.

El objetivo del juego es ordenar los números del 1 al 8 en un tablero de 3x3, moviendo las losetas hacia el espacio vacío. El proyecto incluye algoritmos de inteligencia artificial (IA) para resolver automáticamente el tablero.

### Características Principales

- **Interfaz gráfica intuitiva** desarrollada con Tkinter
- **Dos algoritmos de IA** para resolver el tablero:
  - **A\*** (A-Estrella): Utiliza la distancia Manhattan como función heurística
  - **BFS** (Breadth-First Search): Búsqueda en anchura
- **Contador de movimientos** para seguir el progreso del jugador
- **Soporte para control** tanto con mouse como con teclado
- **Animación de la solución** paso a paso

---

## Estructura del Proyecto

```sh
8-Puzzle-Game-main/
├── README.md                  # Documentación del proyecto
├── requirements.txt            # Dependencias del proyecto
├── run.py                     # Punto de entrada principal
└── src/
    ├── __init__.py            # Archivo de inicialización del paquete
    ├── app.py                 # Lógica de la interfaz gráfica y controladores
    ├── config.py              # Configuración de estilos y colores
    ├── utils.py               # Algoritmos de búsqueda y lógica del juego
    └── assets/
        └── images/
            ├── app.ico        # Icono de la aplicación
            └── tile_0.png
                 tile_1.png
                 tile_2.png
                 tile_3.png
                 tile_4.png
                 tile_5.png
                 tile_6.png
                 tile_7.png
                 tile_8.png    # Imágenes de las losetas del 0 al 8
```

---

## Descripción de Archivos

### Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `run.py` | Punto de entrada del programa. Inicia la aplicación creando una instancia de `OchoRompecabezas` |
| `requirements.txt` | Archivo que contiene las dependencias necesarias para ejecutar el proyecto |

### Directorio `src/`

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Contains the main application classes: `OchoRompecabezas` (main window) and `PaginaRompecabezas` (game page). Maneja la GUI, eventos de usuario y la resolución del tablero |
| `config.py` | Define los colores, fuentes y estilos de todos los widgets de la aplicación |
| `utils.py` | Contains the game logic: `Tablero` class for board operations, `NodoTablero` for the search tree, `A_ESTRELLA` and `BFS` search algorithms |
| `__init__.py` | Archivo vacío que marca el directorio como un paquete de Python |

### Directorio `src/assets/images/`

Contiene las imágenes utilizadas en la interfaz:

- `app.ico`: Icono de la ventana de la aplicación
- `tile_0.png` - `tile_8.png`: Imágenes que representan cada número en el tablero

---

## Dependencias

### Requisitos del Sistema

- **Python 3.0** o superior
- **tkinter**: Incluido por defecto en las instalaciones estándar de Python
- **pillow**: Biblioteca para el manejo de imágenes

### Instalación de Dependencias

Para instalar las dependencias necesarias, ejecute:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` tiene la dependencias necesarias para ejecutar el proyecto:

```sh
pillow==9.2.0
```

---

## Cómo Ejecutar

### Paso 1: Instalar dependencias

Asegúrese de tener Python instalado y luego instale las dependencias:

```bash
pip install pillow --upgrade
```

O simplemente:

```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar el juego

Desde el directorio raíz del proyecto:

```bash
python run.py
```

---

## Cómo Jugar

### Controles

- **Mouse**: Haga clic en una loseta adyacente al espacio vacío para moverla
- **Teclado**: Use las teclas de flecha para mover las losetas
  - Flecha arriba: Mover loseta hacia abajo
  - Flecha abajo: Mover loseta hacia arriba
  - Flecha izquierda: Mover loseta hacia la derecha
  - Flecha derecha: Mover loseta hacia la izquierda

### Botones de Control

| Botón | Función |
|-------|---------|
| **resolver** | Inicia la resolución automática del tablero usando el algoritmo seleccionado |
| **reiniciar** | Reinicia el tablero al último estado barajado |
| **mezclar** | Baraja el tablero generando un nuevo estado aleatorio resoluble |
| **cambiar** | Alterna entre los algoritmos A* y BFS |

### Indicadores

- **Movimientos**: Muestra el número de movimientos realizados
- **Estado**: Muestra el estado actual del juego (Jugando, Resolviendo, Moviendo, Resuelto, Bien hecho!)

---

## Algoritmos de Búsqueda

### A* (A-Estrella)

El algoritmo A* utiliza una función de evaluación que combina:

- **g(n)**: Costo del camino desde el nodo inicial hasta el nodo actual
- **h(n)**: Estimación del costo desde el nodo actual hasta el objetivo (distancia Manhattan)

Formula: `f(n) = g(n) + h(n)`

A* es completo y óptimo cuando la heurística es admisible (nunca sobrestima el costo real).

### BFS (Breadth-First Search)

BFS explora uniformemente todos los nodos al mismo nivel de profundidad antes de pasar al siguiente nivel. Garantiza encontrar la solución óptima en términos de número de movimientos, pero puede ser mucho más lento que A*.

### Comparación

| Algoritmo | Velocidad | Profundidad de Búsqueda | Nodos Expandidos |
|-----------|-----------|------------------------|------------------|
| A*        | Rápido    | Menor                 | Menor            |
| BFS       | Lento     | Mayor                 | Mayor           |

---

## Referencia Académica

Kunkle D. (2001, October 8). [Solving the 8 Puzzle in a Minimum Number of Moves: An Application of the A* Algorithm](https://web.mit.edu/6.034/wwwbob/EightPuzzle.pdf).

---

## Licencia

Este proyecto es de uso educativo.
