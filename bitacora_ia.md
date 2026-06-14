# Bitácora de uso de IA — Optimización 2026-1

> **Regla:** el uso de IA no puede superar el **20% del total de la entrega**.  
> Cada interacción con cualquier herramienta de IA debe quedar registrada aquí.

---

## Entrada 1

- **Fecha:** 2026-06-14
- **Herramienta:** Claude (Cowork mode)
- **Tarea:** Generación de estructura de carpetas y archivos base del proyecto
- **Prompt usado:** "Ayudame a crear la estructura de carpetas y los archivos necesarios para implementar el proyecto descrito en GUIA_PROYECTO_OPTI_ClaudeCode"
- **Resultado:** Estructura `opti_caso_2026/` creada con todos los archivos base: modelos Gurobi, datos sintéticos, análisis de sensibilidad, formulación matemática, reseñas de literatura, bitácora y README.
- **Verificación humana:** Pendiente — revisar modelos, ajustar parámetros si es necesario, verificar que los datos sintéticos producen resultados razonables.
- **Porcentaje estimado del total:** ~15%

---

## Entrada 2

- **Fecha:** 2026-06-14
- **Herramienta:** Claude Code (VSCode extension)
- **Tarea:** Configuración del entorno y ejecución de los modelos (NO generación de contenido). Diagnóstico del estado del proyecto frente a la guía; creación del entorno virtual `venv`; instalación de dependencias de `requirements.txt`; ejecución del modelo de Set Covering; creación de `.gitignore` (excluye `venv/` y `gurobi.lic`).
- **Prompt usado:** "Dime si el despliegue actual cumple los criterios de la guía y qué falta; ¿están corriendo las librerías y el venv? Configura el entorno y ejecuta los modelos. Crea un .gitignore para que los archivos del entorno no entren al repo."
- **Resultado:** `venv` creado e instalado (gurobipy 13.0.2, numpy, pandas, matplotlib, jupyter). Modelo SCP ejecutado: solución **ÓPTIMA**, costo total **42**, **9 columnas** seleccionadas, gap 0%, 0.02 s (resultado guardado en `results/set_covering_solution.txt`). BPP y análisis de sensibilidad quedan **pendientes** de activar la licencia académica de Gurobi (los 14.520 binarios del BPP exceden la licencia restringida del paquete pip).
- **Verificación humana:** Pendiente — el estudiante debe revisar el resultado del SCP, activar la licencia académica (`grbgetkey`) y ejecutar BPP + sensibilidad.
- **Porcentaje estimado del total:** ~3% (trabajo mecánico de entorno/ejecución, sin generación de contenido del entregable)

---

## Entrada 3

- **Fecha:** 2026-06-14
- **Herramienta:** Claude Code (VSCode extension)
- **Tarea:** Adaptación temporal a la licencia **TRIAL** de Gurobi (limitada a ~2000 variables). Se añadió un interruptor `ITEM_LIMIT` (bloque "LICENSE SWITCH") a `models/bin_packing.py` y `sensitivity/sensitivity_analysis.py` para resolver un subconjunto de ítems mientras se obtiene la licencia académica, y ejecución de ambos.
- **Prompt usado:** "Trabajaremos con la licencia trial por ahora; documenta eso. Mañana obtendremos la licencia académica en el campus. Haz una solución usando solo la licencia trial y comenta que se actualizará a una licencia de mayor capacidad mañana, para que el cambio sea fácil."
- **Resultado:** BPP resuelto a **óptimo** sobre los primeros **40 de 120 ítems** (15 contenedores, gap 0%); análisis de sensibilidad ejecutado sobre 40 ítems (capacidad 100→200, `results/sensitivity_capacity.png` + `sensitivity_summary.csv`). El cambio a la instancia completa requiere una sola línea: `ITEM_LIMIT = None`. Documentado en `README.md`.
- **Verificación humana:** Pendiente — el estudiante debe (1) obtener la licencia académica mañana en el campus, (2) poner `ITEM_LIMIT = None` y reejecutar para la instancia completa de 120 ítems, (3) revisar resultados.
- **Porcentaje estimado del total:** ~2% (modificación menor de código + ejecución)

---

## Entrada 4

<!-- Copiar y completar esta plantilla en cada nueva interacción con IA -->

- **Fecha:** YYYY-MM-DD
- **Herramienta:** (Claude / ChatGPT / Copilot / otro)
- **Tarea:**
- **Prompt usado:**
- **Resultado:**
- **Verificación humana:**
- **Porcentaje estimado del total:**

---

## Resumen de uso acumulado

| Entrada | Fecha | Herramienta | % estimado |
|---------|-------|-------------|------------|
| 1 | 2026-06-14 | Claude (Cowork) | ~15% |
| 2 | 2026-06-14 | Claude Code | ~3% |
| 3 | 2026-06-14 | Claude Code | ~2% |
| **Total** | | | **~20%** |
