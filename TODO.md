# TODO - Implementar Objetivo Aleatorio para 8-Puzzle

## Tareas a completar:

1. [x] Modificar `src/core/tablero.py`
   - [x] Agregar método `crear_objetivo_aleatorio()` 
   - [x] Modificar método `resolver()` para aceptar parámetro `objetivo`

2. [x] Modificar `src/core/nodos.py`
   - [x] Modificar `__init__` de `NodoTablero` para aceptar parámetro `objetivo`

3. [x] Modificar `src/gui/game_page.py`
   - [x] Agregar mini-tablero (mismo tamaño que el principal) para mostrar objetivo
   - [x] Agregar botón "Cambiar Objetivo" 
   - [x] Actualizar `Tablero.resolver()` para pasar el objetivo
   - [x] Crear método para actualizar visualización del objetivo

