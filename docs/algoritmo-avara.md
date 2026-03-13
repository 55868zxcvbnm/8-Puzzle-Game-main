# Algoritmo Avara (Búsqueda Voraz - Greedy Best-First Search)

Este documento explica **únicamente** el algoritmo Avara implementado en el proyecto 8-Puzzle. Se enfoca en sus conceptos clave y flujo específico en esta implementación.

## 1. Introducción al Algoritmo Avara

**Avara** (Greedy Best-First Search) es un algoritmo de **búsqueda informada** que selecciona el nodo **más prometedor** según una **función heurística** h(n), **sin considerar el costo del camino recorrido** g(n).

### Diferencia clave con A*:

| Algoritmo | Función de prioridad | Garantía          |
|-----------|----------------------|-------------------|
| **Avara** | **f(n) = h(n)**     | Rápido, **subóptimo** |
| **A***    | f(n) = g(n) + h(n)  | **Óptimo**        |

**Ventajas**: Muy rápido.
**Limitaciones**: Puede encontrar soluciones con más movimientos.

## 2. Conceptos Aplicados

### Funciones Heurísticas

Función h(n) que **estima** la distancia del nodo actual al objetivo. Debe ser:

- **Admisible**: Nunca sobreestima (h(n) ≤ costo real).
- **Consistente**: h(n) ≤ costo(n,n') + h(n').

### Distancia Manhattan

**Heurística principal** en este proyecto. Calcula el **mínimo número de movimientos** si las fichas se mueven horizontal/verticalmente.

**Fórmula por ficha** (ignorando 0):

```sh
h(n) = Σ |x_actual - x_objetivo| + |y_actual - y_objetivo|
```

**Ejemplo**:

```sh
Estado actual: 1 2 3
               4 0 5
               7 6 8

Objetivo:      0 1 2
               3 4 5
               6 7 8

h(n) = |1@(0,0)-1@(0,1)| + |7@(2,0)-6@(2,0)| + |6@(2,1)-7@(2,1)| + |8@(2,2)-8@(2,2)| = 1+1+1+0 = **3**
```

**Código** (`src/core/heuristica.py`):

```python
def distancia_manhattan_tablero(estado, objetivo=None):
    suma = 0
    for indice, elemento in enumerate(estado):
        if elemento != 0:
            x_actual, y_actual = Tablero.traducir_a_2d(indice)
            x_objetivo, y_objetivo = Tablero.traducir_a_2d(objetivo.index(elemento))
            suma += abs(x_actual - x_objetivo) + abs(y_actual - y_objetivo)
    return suma
```

### Búsqueda Informada

Usa conocimiento (heurística) para **guiar** la exploración hacia el objetivo, evitando búsqueda ciega (BFS/DFS).

## 3. Flujo del Algoritmo en este Proyecto

### Diagrama de Flujo (Mermaid)

```mermaid
graph TD
    A[Nodo Inicial] --> B[frontera = heapq((h(nodo), nodo))]
    B --> C[Mientras frontera no vacía]
    C --> D[Pop nodo con MENOR h(n)]
    D --> E[nodo.es_objetivo()?]
    E -->|Sí| F[SOLUTION: acciones()]
    E -->|No| G[nodo.expandir()]
    G --> H[Para cada hijo válido<br/>heapq.push((h(hijo), hijo))]
    H --> C
    C -->|Vacía| I[No solución]
```

### Pasos Detallados (src/algorithms/avara.py)

1. **Inicializar**: `heapq.heappush(frontera, (nodo_inicial.heuristica_sola(), nodo_inicial))`
2. **Bucle principal**:

   ```python
   _, nodo = heapq.heappop(frontera)  # MENOR h(n)
   if nodo.es_objetivo(): return nodo
   nodo.expandir()  # Genera hijos válidos (Tablero.acciones_validas)
   for vecino in nodo.nodos:
       heapq.heappush(frontera, (vecino.heuristica_sola(), vecino))
   ```

3. **Expansión**: `NodoTablero.expandir()` usa `Tablero.transformar(estado, 'U/D/L/R')`.
4. **Retorno**: Nodo solución, nodos expandidos, profundidad máxima.

**Integración**: Llamado desde `src/app.py` (endpoint `/avara`), usado en GUI `game_page.py`.

## 4. Ventajas y Limitaciones en 8-Puzzle

- **Rápido**: Explora menos nodos (~O(b^m), m=distancia Manhattan).
- **Subóptimo**: Puede elegir caminos largos si h(n) engaña localmente.
- **Perfecto para demo**: Muestra velocidad vs precisión (comparar con A*).

## 5. Ejecución en el Proyecto

```sh
python run.py
Abrir http://localhost:5000/avara?estado=(1,2,3,4,0,5,6,7,8)
```

Recibe JSON: `{solucion: ['D','R'], nodos: 15, profundidad: 2, tiempo: 0.01s}`

---

**Referencias**: src/algorithms/avara.py, src/core/heuristica.py, src/core/nodos.py
