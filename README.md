# Optimización 2026-1 — Casos 04 y 07

**Universidad Nacional de Colombia** | Ingeniería de Sistemas y Computación

Problemas: **Bin Packing (BPP)** y **Set Covering (SCP)**  
Solver: **Gurobi 11+ (Python)**

---

## Estructura

```
opti_caso_2026/
├── data/
│   ├── BinPacking_u120_01.txt    # Instancia BPP: 120 items, cap=150
│   └── SetCovering_50x200.txt    # Instancia SCP: 50 filas, 200 columnas
├── models/
│   ├── bin_packing.py            # Modelo ILP — BPP
│   └── set_covering.py           # Modelo ILP — SCP
├── results/                      # Generado al ejecutar los modelos
├── sensitivity/
│   └── sensitivity_analysis.py   # Análisis paramétrico de capacidad (BPP)
├── docs/
│   ├── formulacion_matematica.md
│   └── resenas_literatura.md
├── notebooks/
│   └── exploracion.ipynb
├── bitacora_ia.md
├── requirements.txt
└── README.md
```

## Setup (instalación desde cero)

Guía completa para dejar el proyecto listo en cualquier máquina.

### Requisitos previos

| Herramienta | Versión | Notas |
|-------------|---------|-------|
| Python | 3.10+ | `python --version` |
| pip | reciente | viene con Python |
| Gurobi | 11+ | se instala con `pip` (paso 2); la **licencia** se obtiene aparte (paso 3) |

### Paso 1 — Crear y activar el entorno virtual (`venv`)

Desde la carpeta raíz del proyecto (`opti_caso_2026/`):

```powershell
# Crear el entorno
python -m venv venv

# Activar — Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Activar — Windows (CMD):           .\venv\Scripts\activate.bat
# Activar — macOS / Linux (bash):    source venv/bin/activate
```

> Si PowerShell bloquea la activación con un error de *execution policy*, ejecuta una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelve a intentar.

Con el entorno activado, el prompt muestra `(venv)`. El entorno **no** se sube al repositorio
(está en `.gitignore`).

### Paso 2 — Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Esto instala `gurobipy`, `numpy`, `pandas`, `matplotlib` y `jupyter`.

### Paso 3 — Licencia de Gurobi

El paquete `gurobipy` de `pip` ya incluye un **solver completo**, pero necesita una licencia.
Hay dos opciones:

**Opción A — Licencia académica (recomendada, gratis e ilimitada).**
Necesaria para el BPP completo (120 ítems = 14 520 variables).

1. Regístrate con tu correo `@unal.edu.co` en el portal:
   https://portal.gurobi.com/iam/licenses/request
2. Elige **"Named-User Academic"** (NO "Evaluation/Trial").
3. Descarga e instala el **Gurobi Optimizer** (incluye la herramienta `grbgetkey`):
   https://www.gurobi.com/downloads/gurobi-software/
4. Activa la licencia (idealmente **conectado a la red del campus UNAL** o VPN):
   ```powershell
   grbgetkey <TU-CLAVE-ACADÉMICA>
   ```
   Esto escribe `gurobi.lic` en tu carpeta de usuario.

**Opción B — Licencia trial de `pip` (sin pasos extra, pero limitada a ~2000 variables).**
Funciona inmediatamente para el SCP completo y para el BPP/sensibilidad en modo reducido
(`ITEM_LIMIT = 40`). Ver la sección **"Licencia Gurobi — estado actual"** más abajo.

### Paso 4 — Verificar la instalación

```powershell
# ¿Se importan las librerías y qué versión de Gurobi hay?
python -c "import gurobipy; print('gurobipy', gurobipy.gurobi.version())"

# ¿La licencia permite modelos grandes? (resuelve un modelo de 15000 variables)
python -c "import gurobipy as gp; m=gp.Model(); x=m.addVars(15000, vtype='B'); m.addConstr(x.sum()>=1); m.optimize(); print('LICENCIA COMPLETA OK')"
```

- Si el segundo comando imprime `LICENCIA COMPLETA OK` → tienes la licencia académica (instancia
  completa disponible).
- Si falla con *"Model too large for size-limited license"* → estás en la licencia **trial**;
  usa el modo reducido descrito en la sección **"Licencia Gurobi — estado actual"**.

## Ejecución

```powershell
# Modelo Bin Packing
python models/bin_packing.py

# Modelo Set Covering
python models/set_covering.py

# Análisis de sensibilidad (tarda varios minutos)
python sensitivity/sensitivity_analysis.py
```

## Licencia Gurobi — estado actual (temporal)

> ⚠️ **Estamos usando una licencia TRIAL (limitada a ~2000 variables).** Se actualizará a la
> licencia **académica (ilimitada)** el **15 de junio de 2026** desde la red del campus UNAL.

Implicaciones y resultados con la licencia trial:

| Modelo | Tamaño | ¿Corre con trial? | Estado actual |
|--------|--------|-------------------|---------------|
| **SCP** (50×200) | 200 vars | ✅ Sí | Resuelto a **óptimo** (costo 42, 9 columnas), instancia completa |
| **BPP** (120 ítems) | 14 520 vars | ❌ Excede el límite | Resuelto sobre **subconjunto de 40 ítems** (óptimo: 15 contenedores) |
| **Sensibilidad** (BPP) | igual que BPP | ❌ Excede el límite | Barrido sobre los **40 ítems** (capacidad 100→200) |

### Cómo cambiar a la licencia académica (mañana)

1. Activar la licencia académica: `grbgetkey <CLAVE-ACADÉMICA>` (red del campus UNAL).
2. En `models/bin_packing.py` y `sensitivity/sensitivity_analysis.py`, buscar el bloque
   **`LICENSE SWITCH`** y cambiar una sola línea:
   ```python
   ITEM_LIMIT = 40      # licencia trial
   ITEM_LIMIT = None    # licencia académica -> instancia completa de 120 ítems
   ```
3. Volver a ejecutar los dos scripts. No se requiere ningún otro cambio.

## Entrega

Checklist de la guía: `GUIA_PROYECTO_OPTI_ClaudeCode.md` (directorio padre).  
Fecha límite: **15 de junio de 2026, 11:59 PM**.
