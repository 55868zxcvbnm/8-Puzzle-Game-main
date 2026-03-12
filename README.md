# Juego del 8-Puzzle

## Descripción General

Este proyecto es una implementación del clásico juego de tablero 8-Puzzle desarrollado en Python utilizando la biblioteca **Tkinter** para la interfaz gráfica de usuario.

El objetivo del juego es ordenar los números del 1 al 8 en un tablero de 3x3, moviendo las losetas hacia el espacio vacío. El proyecto incluye algoritmos de inteligencia artificial (IA) para resolver automáticamente el tablero.

### Características Principales

- **Interfaz gráfica intuitiva** desarrollada con Tkinter
- **Tres algoritmos de IA** para resolver el tablero:
  - **A\*** (A-Estrella): Óptimo, usa distancia Manhattan como heurística
  - **Avara** (Greedy): Rápido pero puede no ser óptimo
  - **BFS** (Breadth-First Search): Búsqueda en anchura
- **Contador de movimientos** para seguir el progreso del jugador
- **Soporte para control** tanto con mouse como con teclado
- **Animación de la solución** paso a paso

---

## Estructura del Proyecto

```
8-Puzzle-Game-main/
├── README.md              # Documentación del proyecto
├── requirements.txt       # Dependencias del proyecto
├── run.py                 # Punto de entrada principal
└── src/
    ├── __init__.py
    ├── app.py             # Lógica de la interfaz gráfica
    ├── config.py          # Configuración de estilos y colores
    ├── utils.py           # Compatibilidad - re-exporta desde core
    ├── algorithms/        # Algoritmos de búsqueda
    │   ├── __init__.py
    │   ├── a_estrella.py # Algoritmo A*
    │   ├── avara.py      # Algoritmo Greedy
    │   └── bfs.py        # Algoritmo BFS
    ├── core/             # Núcleo del juego
    │   ├── __init__.py
    │   ├── tablero.py    # Clase Tablero
    │   ├── nodos.py     # Clases Nodo, NodoTablero
    │   └── heuristica.py# Funciones heurísticas
    ├── gui/              # Interfaz gráfica (opcional)
    │   ├── __init__.py
    │   ├── main_window.py
    │   └── game_page.py
    └── assets/
        └── images/
            ├── app.ico
            └── tile_0.png ... tile_8.png
```

---

## Descripción de Archivos

### Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `run.py` | Punto de entrada del programa. Inicia la aplicación |
| `requirements.txt` | Dependencias necesarias (pillow) |

### Directorio `src/`

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Clase principal `OchoRompecabezas` y `PaginaRompecabezas`. Maneja la GUI y resolución del tablero |
| `config.py` | Colores, fuentes y estilos de la aplicación |
| `utils.py` | Módulo de compatibilidad que re-exporta desde `core` |

### Directorio `src/algorithms/`

| Archivo | Descripción |
|---------|-------------|
| `a_estrella.py` | Algoritmo A* (óptimo) |
| `avara.py` | Algoritmo Greedy (rápido) |
| `bfs.py` | Algoritmo BFS (anchura) |

### Directorio `src/core/`

| Archivo | Descripción |
|---------|-------------|
| `tablero.py` | Clase `Tablero` con operaciones del tablero |
| `nodos.py` | Clases `Nodo` y `NodoTablero` para el árbol de búsqueda |
| `heuristica.py` | Funciones heurísticas (distancia Manhattan) |

### Directorio `src/assets/images/`

- `app.ico`: Icono de la ventana
- `tile_0.png` - `tile_8.png`: Imágenes de las losetas

---

## Dependencias

### Requisitos del Sistema

- **Python 3.0** o superior
- **tkinter**: Incluido por defecto en Python
- **pillow**: Biblioteca para imágenes

### Instalación

```bash
pip install -r requirements.txt
```

---

## Cómo Ejecutar

```bash
python run.py
```

---

## Cómo Jugar

### Controles

- **Mouse**: Clic en loseta adyacente al espacio vacío
- **Teclado**: Flechas para mover las losetas

### Botones

| Botón | Función |
|-------|---------|
| **resolver** | Resuelve automáticamente el tablero |
| **reiniciar** | Reinicia al último estado barajado |
| **mezclar** | Baraja el tablero |
| **cambiar** | Alterna entre algoritmos |

---

## Algoritmos de Búsqueda

### A* (A-Estrella)
- **Función**: f(n) = g(n) + h(n)
- **Características**: Óptimo y completo con heurística admisible

### Avara (Greedy)
- **Función**: f(n) = h(n)
- **Características**: Rápido pero puede no ser óptimo

### BFS (Breadth-First Search)
- **Características**: Garantiza solución con menos movimientos pero puede ser lento

### Comparación

| Algoritmo | Velocidad | Optimalidad |
|-----------|-----------|-------------|
| A*        | Media     | Sí          |
| Avara     | Rápida    | No          |
| BFS       | Lenta     | Sí          |

---

## Licencia

Este proyecto es de uso educativo.

