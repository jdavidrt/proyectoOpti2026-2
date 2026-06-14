# Guía de proyecto — Optimización 2026-1 con Claude Code + VSCode (Windows)

**Universidad Nacional de Colombia** | Ingeniería de Sistemas y Computación  
Problemas: **04 Bin Packing** y **07 Set Covering**  
Herramienta de solución: **Gurobi (Python)**

---

## Requisitos previos

| Herramienta | Versión mínima | Enlace |
|-------------|---------------|--------|
| VS Code | 1.98.0 | https://code.visualstudio.com |
| Node.js | 18+ | https://nodejs.org |
| Python | 3.10+ | https://python.org |
| Gurobi | 11+ | https://gurobi.com (licencia académica gratuita) |
| Cuenta Anthropic | Claude Pro o Max | https://claude.ai |

> **Nota:** Claude Code corre nativamente en Windows desde finales de 2025. No necesitas WSL2.

---

## Paso 1 — Instalar Claude Code en VSCode

1. Abre VSCode.
2. Presiona `Ctrl+Shift+X` para abrir el panel de extensiones.
3. Busca **"Claude Code"** — instala la extensión publicada por **Anthropic**.
4. Reinicia VSCode si se solicita.
5. Haz clic en el ícono **Spark (⚡)** en la barra lateral izquierda para abrir Claude Code.
6. Inicia sesión con tu cuenta Anthropic cuando se solicite (OAuth).

---

## Paso 2 — Instalar Claude Code CLI (opcional pero recomendado)

Abre una terminal PowerShell en VSCode (`Ctrl+\``) y ejecuta:

```powershell
npm install -g @anthropic-ai/claude-code
```

Verifica la instalación:

```powershell
claude --version
```

---

## Paso 3 — Estructura del proyecto

Crea la siguiente estructura de carpetas manualmente o pídele a Claude Code que la genere:

```
opti_caso_2026/
│
├── data/
│   ├── BinPacking_u120_01.txt        # Datos del problema 4
│   └── SetCovering_50x200.txt        # Datos del problema 7
│
├── models/
│   ├── bin_packing.py                # Modelo Gurobi — BPP
│   └── set_covering.py               # Modelo Gurobi — SCP
│
├── results/
│   ├── bin_packing_solution.txt      # Salida del solver
│   └── set_covering_solution.txt
│
├── sensitivity/
│   └── sensitivity_analysis.py       # Análisis de sensibilidad
│
├── docs/
│   ├── formulacion_matematica.md     # Formulaciones LaTeX
│   └── resenas_literatura.md         # Reseñas por problema
│
├── notebooks/
│   └── exploracion.ipynb             # Análisis exploratorio opcional
│
├── bitacora_ia.md                    # Bitácora de uso de IA (OBLIGATORIO)
├── requirements.txt
└── README.md
```

Para que Claude Code genere esto automáticamente, escribe en el panel Spark:

```
Create the full folder structure for an optimization project with two problems:
Bin Packing (BPP) and Set Covering (SCP). Use Python + Gurobi.
Include folders: data, models, results, sensitivity, docs, notebooks.
Add empty placeholder files in each folder.
```

---

## Paso 4 — Configurar el entorno Python

En la terminal de VSCode:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install dependencies
pip install gurobipy numpy pandas matplotlib jupyter
```

Crea el archivo `requirements.txt`:

```
gurobipy>=11.0
numpy>=1.26
pandas>=2.0
matplotlib>=3.8
jupyter>=1.0
```

---

## Paso 5 — Obtener la licencia académica de Gurobi

1. Ve a https://gurobi.com/academia/academic-program-and-licenses/
2. Regístrate con tu correo `@unal.edu.co`.
3. Descarga la licencia y ejecuta en PowerShell:

```powershell
grbgetkey TU-CLAVE-AQUI
```

Verifica que funciona:

```powershell
python -c "import gurobipy; print(gurobipy.gurobi.version())"
```

---

## Paso 6 — Conseguir los archivos de datos

### Bin Packing — instancia Falkenauer u120_01

Fuente: OR-Library (Beasley) — http://people.brunel.ac.uk/~mastjjb/jeb/orlib/binpackinfo.html

Formato del archivo:
```
# Line 1: number of test cases
# For each test case:
#   Line 1: number of items, bin capacity, optimal solution
#   Lines 2..n+1: item weights (one per line)
```

### Set Covering — instancia 50x200

Fuente: OR-Library — http://people.brunel.ac.uk/~mastjjb/jeb/orlib/scpinfo.html

Formato del archivo:
```
# Line 1: number of rows (m), number of columns (n)
# Line 2: cost of each column j (n values)
# For each row i: number of columns that cover it, then column indices
```

Si no consigues los archivos, dile a Claude Code:

```
Write a Python script that generates a synthetic Bin Packing instance
with 120 items, bin capacity 150, weights uniformly distributed in [20, 100].
Save it to data/BinPacking_u120_01.txt in OR-Library format.
```

---

## Paso 7 — Desarrollar los modelos con Claude Code

### Flujo de trabajo con Claude Code en VSCode

Abre el archivo `models/bin_packing.py` y luego haz clic en el ícono **Spark** en la esquina superior derecha del editor. Escribe tu prompt directamente en contexto del archivo abierto.

#### Prompt para el modelo de Bin Packing:

```
I need a Gurobi Python model for the 1D Bin Packing Problem (BPP).

Decision variables:
- x[i][j] = 1 if item i is assigned to bin j, 0 otherwise
- y[j] = 1 if bin j is used, 0 otherwise

Objective: minimize sum of y[j]

Constraints:
- Each item assigned to exactly one bin
- Bin capacity not exceeded
- x[i][j] <= y[j] for all i, j (linking constraint)
- Binary variables

The model must:
1. Read data from data/BinPacking_u120_01.txt
2. Build and solve the Gurobi model
3. Print: number of bins used, solution status, solve time
4. Save results to results/bin_packing_solution.txt
5. Include comments explaining each constraint mathematically
```

#### Prompt para el modelo de Set Covering:

```
I need a Gurobi Python model for the Set Covering Problem (SCP).

Decision variables:
- x[j] = 1 if column j is selected, 0 otherwise

Objective: minimize sum of c[j] * x[j]

Constraints:
- For each row i: sum of x[j] for j covering i >= 1

The model must:
1. Read data from data/SetCovering_50x200.txt
2. Build and solve the Gurobi model
3. Print: total cost, number of columns selected, solve time
4. Save results to results/set_covering_solution.txt
5. Include comments explaining each constraint
```

---

## Paso 8 — Análisis de sensibilidad

Abre `sensitivity/sensitivity_analysis.py` con el contexto del modelo de Bin Packing activo. Prompt para Claude Code:

```
Write a sensitivity analysis script for the Bin Packing model.
Vary the bin capacity C from 100 to 200 in steps of 10.
For each value of C, solve the model and record:
- Number of bins used
- Solve time
- Optimality gap (if any)
Plot the results using matplotlib: bins used vs capacity.
Save the plot to results/sensitivity_capacity.png
```

---

## Paso 9 — Generar el documento de formulación matemática

Crea `docs/formulacion_matematica.md` con Claude Code:

```
Write the formal mathematical formulation in LaTeX (using $$ notation) for:

1. 1D Bin Packing Problem:
   - Sets and parameters
   - Decision variables with domain
   - Objective function
   - All constraints with names and explanations
   - Problem classification (ILP, NP-hard, etc.)

2. Set Covering Problem:
   - Same structure as above

Format as a clean Markdown document with LaTeX math blocks.
Language: Spanish.
```

---

## Paso 10 — Bitácora de IA (obligatorio)

El documento `bitacora_ia.md` debe registrar **cada vez que uses IA**, incluyendo Claude Code. Ejemplo de estructura:

```markdown
# Bitácora de uso de IA — Optimización 2026-1

## Entrada 1
- Fecha: YYYY-MM-DD
- Herramienta: Claude Code (VSCode extension)
- Tarea: Generación de estructura de carpetas del proyecto
- Prompt usado: "Create the full folder structure..."
- Resultado: Estructura creada en /opti_caso_2026/
- Verificación humana: Sí — se revisó y ajustó manualmente
- Porcentaje estimado del total: ~2%

## Entrada 2
...
```

> Recuerda: el uso de IA no puede superar el **20% del total de la entrega**.

---

## Atajos clave de Claude Code en VSCode

| Acción | Atajo |
|--------|-------|
| Abrir Claude Code | Clic en ícono Spark ⚡ |
| Nueva conversación | `Ctrl+N` en el panel Claude |
| Mencionar un archivo | Escribe `@` seguido del nombre |
| Ver historial | Panel lateral de Claude Code |
| Aceptar cambio | Botón "Accept" en el diff inline |
| Rechazar cambio | Botón "Reject" en el diff inline |

---

## Checklist de entrega (15 de junio, 11:59 PM)

- [ ] Formulación matemática — Bin Packing
- [ ] Formulación matemática — Set Covering
- [ ] Reseña de literatura — Bin Packing (máx. 1 página)
- [ ] Reseña de literatura — Set Covering (máx. 1 página)
- [ ] Modelo Gurobi funcionando — Bin Packing
- [ ] Modelo Gurobi funcionando — Set Covering
- [ ] Captura de pantalla del resultado de Gurobi (como anexo)
- [ ] Análisis de sensibilidad (mínimo un problema)
- [ ] Análisis de resultados e implicaciones
- [ ] Conclusiones
- [ ] Bitácora de uso de IA con prompts incluidos
- [ ] Archivos de código adjuntos (.py)
- [ ] Documento principal en PDF o Word

---

## Recursos de referencia

| Recurso | URL |
|---------|-----|
| Docs Claude Code VSCode | https://code.claude.com/docs/en/vs-code |
| OR-Library (datos) | http://people.brunel.ac.uk/~mastjjb/jeb/orlib |
| Gurobi Python docs | https://docs.gurobi.com/projects/optimizer/en/current/reference/python |
| Gurobi licencia académica | https://gurobi.com/academia |
| Bin Packing — referencia clásica | Falkenauer (1996), European Journal of Operational Research |
| Set Covering — referencia clásica | Beasley (1987), European Journal of Operational Research |
