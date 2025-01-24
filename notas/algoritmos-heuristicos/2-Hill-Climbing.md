# Hill Climbing

El **algoritmo Hill Climbing** (o "Escalada de Colinas") es
un método de optimización y búsqueda local utilizado para encontrar
soluciones aproximadas a problemas de maximización o minimización.
Es un algoritmo **heurístico** que parte de una solución inicial y
realiza mejoras iterativas hasta alcanzar un óptimo local. A
continuación, te lo explico a detalle:

---

## **Concepto Básico**

La idea central del Hill Climbing es similar a escalar una colina en
la oscuridad: te mueves en la dirección que parece ascender (maximizar)
o descender (minimizar) hasta que no puedas mejorar más. Es un algoritmo
**codicioso** (greedy), ya que siempre toma la decisión que parece mejor
en el momento, sin considerar el panorama global.

---

## **Pasos del Algoritmo**

### Problema de las 8 reinas

El **problema de las 8 reinas** es un desafío clásico en matemáticas,
ciencias de la computación y teoría de juegos. Consiste en colocar **8
reinas** en un tablero de ajedrez estándar (8x8 casillas) de tal manera
que ninguna reina pueda atacar a otra. Es decir, ninguna reina puede
compartir la misma fila, columna o diagonal con otra reina.

---

### **¿Por qué es difícil?**

- **Reglas del ajedrez**: Una reina puede moverse cualquier número de
  casillas en horizontal, vertical o diagonal.
- **Combinatorialidad**: Hay \( \binom{64}{8} \approx 4.4 \times
  10^9 \) formas de colocar 8 reinas en el tablero, pero solo
  **92 soluciones válidas** (considerando simetrías y rotaciones,
  son 12 soluciones únicas).
- **Restricciones estrictas**: Cada reina debe estar en una fila, columna
  y diagonales únicas.

---

### **Reglas del problema**

1. **Ninguna reina en la misma fila**.
2. **Ninguna reina en la misma columna**.
3. **Ninguna reina en la misma diagonal** (tanto diagonales primarias
   como secundarias).

---

### **Ejemplo de una solución válida**

Aquí hay una configuración válida para las 8 reinas:

```
8 | · · · Q · · · ·
7 | · · · · · Q · ·
6 | · Q · · · · · ·
5 | · · · · · · Q ·
4 | Q · · · · · · ·
3 | · · Q · · · · ·
2 | · · · · Q · · ·
1 | · · · · · · · Q
  ------------------
    a b c d e f g h
```

- **Coordenadas** (fila, columna):
  - (0, 0), (1, 4), (2, 7), (3, 5), (4, 2), (5, 6), (6, 1), (7, 3).

### Pasos del algoritmo aplicados a dos problemas

Se abordarán estos pasos con la maximización de una función continua
y el problema de las 8 reinas. Las formulas de la función están en
formato `LaTeX`

#### **1. Inicialización**

- **Objetivo**: Generar una solución inicial, que puede ser aleatoria o
  basada en algún criterio.
- **Ejemplo**:
  - En una función matemática: \( x\_{\text{inicial}} = 0 \).
  - En las 8-reinas: Colocar 8 reinas aleatoriamente en el tablero,
    una por columna.

#### **2. Evaluación**

- **Objetivo**: Calcular la calidad de la solución actual usando una
  **función
  de evaluación** (o _fitness_).
- **Ejemplo**:
  - Función \( f(x) = -x^2 + 4x \): Calcular \( f(x\_{\text{inicial}}) \).
  - 8-reinas: Contar el número de **pares de reinas no atacantes**
    (heurística a maximizar).

#### **3. Generación de Vecinos**

- **Objetivo**: Crear soluciones cercanas modificando ligeramente la
  solución actual.
- **Ejemplo**:
  - Función continua: \( x\_{\text{vecino}} = x \pm \Delta \)
    (por ejemplo, \( \Delta = 0.5 \)).
  - 8-reinas: Mover una reina a otra fila dentro de su columna
    (generar todos los posibles movimientos).

#### **4. Selección del Mejor Vecino**

- **Objetivo**: Evaluar todos los vecinos y seleccionar el que tenga la
  mejor calidad.
- **Ejemplo**:
  - Función: Elegir el \( x\_{\text{vecino}} \) con mayor \( f(x) \).
  - 8-reinas: Elegir el movimiento que maximice los pares no atacantes.

#### **5. Decisión**

- **Objetivo**: Si el mejor vecino es mejor que la solución actual,
  reemplazarla. Si no, terminar.
- **Condición de parada**: No hay vecinos mejores (se alcanzó un
  **óptimo local**).

---

### **Ejemplo 1: Maximizando una Función Continua**

**Función**: \( f(x) = -x^2 + 4x \) (máximo global en \( x = 2 \), \( f(2) = 4 \)).  
**Paso de exploración**: \( \Delta = 0.5 \).

#### **Iteración 1**

| Paso                | Detalle                                      |
| ------------------- | -------------------------------------------- |
| **Solución actual** | \( x = 0 \) → \( f(0) = 0 \)                 |
| **Generar vecinos** | \( x = 0.5 \) y \( x = -0.5 \)               |
| **Evaluar vecinos** | \( f(0.5) = 1.75 \), \( f(-0.5) = -2.25 \)   |
| **Selección**       | Mejor vecino: \( x = 0.5 \)                  |
| **Decisión**        | \( 1.75 > 0 \) → Actualizar a \( x = 0.5 \). |

#### **Iteración 2**

| Paso                | Detalle                                      |
| ------------------- | -------------------------------------------- |
| **Solución actual** | \( x = 0.5 \) → \( f(0.5) = 1.75 \)          |
| **Generar vecinos** | \( x = 1.0 \) y \( x = 0.0 \)                |
| **Evaluar vecinos** | \( f(1.0) = 3 \), \( f(0.0) = 0 \)           |
| **Selección**       | Mejor vecino: \( x = 1.0 \)                  |
| **Decisión**        | \( 3 > 1.75 \) → Actualizar a \( x = 1.0 \). |

#### **Iteración 3**

| Paso                | Detalle                                      |
| ------------------- | -------------------------------------------- |
| **Solución actual** | \( x = 1.0 \) → \( f(1.0) = 3 \)             |
| **Generar vecinos** | \( x = 1.5 \) y \( x = 0.5 \)                |
| **Evaluar vecinos** | \( f(1.5) = 3.75 \), \( f(0.5) = 1.75 \)     |
| **Selección**       | Mejor vecino: \( x = 1.5 \)                  |
| **Decisión**        | \( 3.75 > 3 \) → Actualizar a \( x = 1.5 \). |

#### **Iteración 4**

| Paso                | Detalle                                      |
| ------------------- | -------------------------------------------- |
| **Solución actual** | \( x = 1.5 \) → \( f(1.5) = 3.75 \)          |
| **Generar vecinos** | \( x = 2.0 \) y \( x = 1.0 \)                |
| **Evaluar vecinos** | \( f(2.0) = 4 \), \( f(1.0) = 3 \)           |
| **Selección**       | Mejor vecino: \( x = 2.0 \)                  |
| **Decisión**        | \( 4 > 3.75 \) → Actualizar a \( x = 2.0 \). |

#### **Iteración 5**

| Paso                | Detalle                                         |
| ------------------- | ----------------------------------------------- |
| **Solución actual** | \( x = 2.0 \) → \( f(2.0) = 4 \)                |
| **Generar vecinos** | \( x = 2.5 \) y \( x = 1.5 \)                   |
| **Evaluar vecinos** | \( f(2.5) = 3.75 \), \( f(1.5) = 3.75 \)        |
| **Selección**       | Ningún vecino es mejor → **Algoritmo termina**. |

**Resultado**: Se alcanzó el máximo global en \( x = 2 \).

---

### **Ejemplo 2: Problema de las 8-Reinas**

**Objetivo**: Colocar 8 reinas en un tablero de ajedrez sin que se
ataquen.

**Heurística**: Número de pares de reinas **no atacantes** (valor a
maximizar: máximo = 28 pares).

#### **Iteración 1**

| Paso                | Detalle                                                                 |
| ------------------- | ----------------------------------------------------------------------- |
| **Solución actual** | Configuración inicial aleatoria (ejemplo: 16 pares no atacantes).       |
| **Generar vecinos** | Mover cada reina a todas las filas posibles en su columna (56 vecinos). |
| **Evaluar vecinos** | Calcular pares no atacantes para cada vecino.                           |
| **Selección**       | Elegir el vecino con mayor heurística (ejemplo: 20 pares).              |
| **Decisión**        | \( 20 > 16 \) → Actualizar a la nueva configuración.                    |

#### **Iteración 2**

| Paso                | Detalle                                        |
| ------------------- | ---------------------------------------------- |
| **Solución actual** | Nueva configuración (20 pares no atacantes).   |
| **Generar vecinos** | Mover cada reina nuevamente en su columna.     |
| **Evaluar vecinos** | Encontrar un vecino con 24 pares no atacantes. |
| **Selección**       | Actualizar a la configuración con 24 pares.    |

#### **Iteración 3**

| Paso                | Detalle                                                                               |
| ------------------- | ------------------------------------------------------------------------------------- |
| **Solución actual** | Configuración con 24 pares no atacantes.                                              |
| **Generar vecinos** | Explorar movimientos, pero ningún vecino supera 24.                                   |
| **Decisión**        | **Algoritmo termina** (óptimo local alcanzado, pero no es la solución óptima global). |

**Resultado**: Se encontró una solución con 24 pares no atacantes, pero
no la óptima (28 pares). Esto demuestra la limitación de Hill
Climbing ante óptimos locales.

---

### **Pseudocódigo del Hill Climbing**

```python
def hill_climbing(problema):
    estado_actual = generar_estado_inicial()
    while True:
        vecinos = generar_vecinos(estado_actual)
        if not vecinos:
            break
        mejor_vecino = max(vecinos, key=lambda x: evaluar(x))
        if evaluar(mejor_vecino) <= evaluar(estado_actual):
            break
        estado_actual = mejor_vecino
    return estado_actual
```

---

### **Limitaciones y Soluciones**

1. **Óptimos locales**: Usar **reinicio aleatorio** (ejecutar el algoritmo
   múltiples veces).
2. **Mesetas (plateaus)**: Permitir movimientos laterales (misma
   calidad) con límite de pasos.
3. **Crestas o valles estrechos**: Usar **Simulated Annealing**
   para aceptar movimientos peores temporalmente.

---

### **Conclusión**

El Hill Climbing es ideal para problemas donde:

- El espacio de búsqueda es grande pero no infinito.
- Se necesita una solución rápida, aunque no sea la mejor.
- La función de evaluación es fácil de calcular.

## Su simplicidad lo hace útil en aplicaciones como optimización de parámetros, logística o diseño de redes, aunque siempre debe considerarse el riesgo de quedar atrapado en óptimos locales.

## **Tipos de Hill Climbing**

1. **Hill Climbing Simple**:

   - Elige el **primer vecino** que mejore la solución actual, sin
     evaluar todos los vecinos.
   - Más rápido pero menos preciso.

2. **Hill Climbing de Máxima Pendiente (Steepest-Ascent)**:

   - Evalúa **todos los vecinos** y selecciona el mejor.
   - Más lento pero más preciso.

3. **Hill Climbing Estocástico**:
   - Elige un vecino al **azar**, pero con mayor probabilidad de
     seleccionar aquellos que ofrezcan mejoras.

---

puedes detallas el primer paso?

## **Características Clave**

- **Optimización Local**: Encuentra el óptimo local más cercano a la
  solución inicial, pero no garantiza el óptimo global.
- **Dependencia de la Solución Inicial**: Si la solución inicial
  está cerca de un óptimo local, el algoritmo se quedará allí.
- **Problemas con Máximos/Minimos Locales**: Puede quedar
  "atrapado" en soluciones subóptimas.
- **Problemas con Mesetas (Plataformas)**: Si todos los vecinos
  tienen la misma calidad, el algoritmo no sabe cómo avanzar.
- **Determinista vs. Estocástico**: Dependiendo de la variante,
  puede ser determinista (siempre elige la misma opción) o
  estocástico (incorpora aleatoriedad).

---

## **Aplicaciones**

- Optimización de funciones matemáticas.
- Problemas de planificación y programación.
- Inteligencia Artificial (por ejemplo, ajuste de parámetros en
  redes neuronales).
- Diseño de circuitos o rutas (como el problema del viajante
  simplificado).
- Juegos (como el 8-puzzle o Sudoku).

---

## **Ventajas**

- **Sencillez**: Fácil de implementar y entender.
- **Eficiencia**: Requiere pocos recursos computacionales en cada
  iteración.
- **Rapidez**: Útil para problemas donde una solución aproximada
  es suficiente.

---

## **Desventajas**

- **Óptimos Locales**: No garantiza encontrar la mejor solución
  global.
- **Sensibilidad a la Inicialización**: La calidad de la solución
  final depende de la solución inicial.
- **Problemas con Mesetas o Crestas**: Puede estancarse si no
  hay una dirección clara de mejora.
- **Falta de Retroceso**: Una vez que toma una decisión, no
  puede deshacerla (a diferencia de algoritmos como el
  _Backtracking_).

---

## **Ejemplo Práctico**

Supongamos que queremos maximizar la función \( f(x) = -x^2 + 4x \).
El máximo global está en \( x = 2 \) (con \( f(2) = 4 \)).

1. **Solución inicial**: \( x = 0 \) (\( f(0) = 0 \)).
2. **Generar vecinos**: \( x + 0.5 = 0.5 \), \( x - 0.5 = -0.5 \).
3. **Evaluar vecinos**:
   - \( f(0.5) = -0.25 + 2 = 1.75 \).
   - \( f(-0.5) = -0.25 - 2 = -2.25 \).
4. **Seleccionar mejor vecino**: \( x = 0.5 \).
5. **Repetir** hasta llegar a \( x = 2 \), donde ningún vecino mejora el
   valor.

---

## **Variantes para Mejorar el Hill Climbing**

1. **Hill Climbing con Reinicio Aleatorio**:
   - Ejecuta el algoritmo múltiples veces con soluciones iniciales
     aleatorias y selecciona la mejor solución encontrada.
2. **Simulated Annealing**:
   - Permite moverse ocasionalmente a soluciones peores para escapar
     de óptimos locales, usando una "temperatura" que disminuye con el
     tiempo.
3. **Algoritmos Genéticos**:
   - Combina múltiples soluciones y utiliza operadores como cruce y
     mutación para explorar el espacio de búsqueda.

---

## **Conclusión**

El Hill Climbing es un algoritmo fundamental en optimización heurística,
ideal para problemas donde la solución exacta es computacionalmente costosa.
Aunque tiene limitaciones (como los óptimos locales), su simplicidad y
eficiencia lo hacen útil en muchos contextos prácticos. Para problemas
complejos, suele combinarse con otras técnicas (como reinicios aleatorios o
enfriamiento simulado) para mejorar su rendimiento.
