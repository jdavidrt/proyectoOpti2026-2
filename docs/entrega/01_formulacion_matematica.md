# Formulación Matemática

**Universidad Nacional de Colombia** | Optimización 2026-1
**Autores:** David Ramírez · Jaisson Machado Bautista

---

## 1. Problema de Empaquetamiento en Contenedores (Bin Packing Problem — BPP)

### 1.1 Descripción

El BPP consiste en empacar $n$ objetos con pesos dados en el menor número posible de contenedores homogéneos de capacidad $C$.

### 1.2 Conjuntos y parámetros

| Símbolo | Descripción |
|---------|-------------|
| $I = \{1, \ldots, n\}$ | Conjunto de objetos |
| $J = \{1, \ldots, n\}$ | Conjunto de contenedores (cota superior: $n$) |
| $w_i \in \mathbb{Z}^+$ | Peso del objeto $i$ |
| $C \in \mathbb{Z}^+$ | Capacidad de cada contenedor |

### 1.3 Variables de decisión

$$
x_{ij} = \begin{cases} 1 & \text{si el objeto } i \text{ se asigna al contenedor } j \\ 0 & \text{en caso contrario} \end{cases}
\quad \forall i \in I,\; j \in J
$$

$$
y_j = \begin{cases} 1 & \text{si el contenedor } j \text{ es utilizado} \\ 0 & \text{en caso contrario} \end{cases}
\quad \forall j \in J
$$

### 1.4 Función objetivo

$$
\min \sum_{j \in J} y_j
$$

Se minimiza el número total de contenedores utilizados.

### 1.5 Restricciones

**(R1) Asignación única** — cada objeto debe pertenecer a exactamente un contenedor:

$$
\sum_{j \in J} x_{ij} = 1 \qquad \forall i \in I
$$

**(R2) Capacidad y enlace** — la carga total del contenedor $j$ no puede exceder $C$, y si el contenedor no está abierto ($y_j = 0$) no puede recibir objetos:

$$
\sum_{i \in I} w_i \, x_{ij} \leq C \, y_j \qquad \forall j \in J
$$

**(R3) Dominio binario:**

$$
x_{ij} \in \{0, 1\} \quad \forall i \in I,\; j \in J \qquad y_j \in \{0, 1\} \quad \forall j \in J
$$

**(R4) Ruptura de simetría** *(opcional, mejora el rendimiento del solver)* — los contenedores se ordenan por índice:

$$
y_j \geq y_{j+1} \qquad \forall j \in \{1, \ldots, n-1\}
$$

### 1.6 Clasificación

- Tipo: **Programación Lineal Entera (ILP)**
- Complejidad: **NP-difícil** (reducción desde *partition problem*)
- Variables: $n^2 + n$ binarias
- Restricciones: $n + n + (n-1) = 3n - 1$ (sin contar dominio)

---

## 2. Problema de Cobertura de Conjuntos (Set Covering Problem — SCP)

### 2.1 Descripción

Dado un universo de $m$ elementos (filas) y $n$ subconjuntos (columnas) con costos asociados, se selecciona un subconjunto de columnas de costo mínimo tal que cada fila quede cubierta por al menos una columna seleccionada.

### 2.2 Conjuntos y parámetros

| Símbolo | Descripción |
|---------|-------------|
| $I = \{1, \ldots, m\}$ | Universo de elementos (filas) |
| $J = \{1, \ldots, n\}$ | Conjunto de subconjuntos disponibles (columnas) |
| $c_j \in \mathbb{R}^+$ | Costo de seleccionar la columna $j$ |
| $a_{ij} \in \{0,1\}$ | 1 si la columna $j$ cubre la fila $i$, 0 si no |
| $A(i) = \{j \in J : a_{ij} = 1\}$ | Columnas que cubren la fila $i$ |

### 2.3 Variables de decisión

$$
x_j = \begin{cases} 1 & \text{si la columna } j \text{ es seleccionada} \\ 0 & \text{en caso contrario} \end{cases}
\quad \forall j \in J
$$

### 2.4 Función objetivo

$$
\min \sum_{j \in J} c_j \, x_j
$$

Se minimiza el costo total de las columnas seleccionadas.

### 2.5 Restricciones

**(R1) Cobertura total** — cada fila $i$ debe ser cubierta por al menos una columna seleccionada:

$$
\sum_{j \in A(i)} x_j \geq 1 \qquad \forall i \in I
$$

**(R2) Dominio binario:**

$$
x_j \in \{0, 1\} \qquad \forall j \in J
$$

### 2.6 Formulación matricial equivalente

$$
\min \quad \mathbf{c}^\top \mathbf{x} \qquad \text{s.a.} \quad A\mathbf{x} \geq \mathbf{1},\quad \mathbf{x} \in \{0,1\}^n
$$

donde $A \in \{0,1\}^{m \times n}$ es la matriz de cobertura.

### 2.7 Clasificación

- Tipo: **Programación Lineal Entera (ILP)**
- Complejidad: **NP-difícil** (contiene al problema de cobertura de vértices como caso especial)
- Variables: $n$ binarias
- Restricciones: $m$ restricciones de cobertura

---

## 3. Comparación de formulaciones

| Aspecto | Bin Packing | Set Covering |
|---------|-------------|--------------|
| Variables | $n^2 + n$ | $n$ |
| Restricciones clave | Capacidad + enlace | Cobertura |
| Objetivo | Minimizar contenedores | Minimizar costo |
| Estructura | Asignación 2D | Selección 1D |
| Relajación LP | Débil (brecha integrality alta) | Moderada |
| Simetría | Alta (requiere ruptura) | Baja |
