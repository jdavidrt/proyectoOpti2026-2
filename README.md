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

## Setup

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```powershell
# Modelo Bin Packing
python models/bin_packing.py

# Modelo Set Covering
python models/set_covering.py

# Análisis de sensibilidad (tarda varios minutos)
python sensitivity/sensitivity_analysis.py
```

## Entrega

Checklist de la guía: `GUIA_PROYECTO_OPTI_ClaudeCode.md` (directorio padre).  
Fecha límite: **15 de junio de 2026, 11:59 PM**.
