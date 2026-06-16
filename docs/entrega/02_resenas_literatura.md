# Reseñas de Literatura

**Universidad Nacional de Colombia** | Optimización 2026-1
**Autores:** David Ramírez · Jaisson Machado Bautista

---

## Problema 04 — Bin Packing Problem (BPP)

**Referencia canónica:** Falkenauer, E. (1996). A hybrid grouping genetic algorithm for bin packing. *Journal of Heuristics*, 2(1), 5–30.

**Reseña:**

El artículo de Falkenauer (1996) aborda el BPP unidimensional —uno de los problemas combinatorios más estudiados en optimización— mediante un algoritmo genético híbrido denominado *Grouping Genetic Algorithm* (GGA). A diferencia de los algoritmos genéticos clásicos que codifican asignaciones individuales, el GGA opera directamente sobre grupos (contenedores), lo que reduce drásticamente la simetría del espacio de búsqueda y mejora la convergencia.

El trabajo introduce la instancia de referencia **u120** (120 ítems, distribución uniforme de pesos, capacidad 150), que se convirtió en benchmark estándar de la OR-Library de Beasley. Los resultados reportados muestran soluciones óptimas o cercanas al óptimo en tiempos razonables, superando a heurísticas clásicas como *First Fit Decreasing* (FFD).

Desde la perspectiva de modelos exactos, el BPP puede formularse como un ILP con $O(n^2)$ variables binarias. La principal dificultad computacional proviene de la alta simetría: reordenar los contenedores produce soluciones equivalentes, lo que multiplica el espacio de soluciones sin aportar información nueva. Técnicas como la restricción de ordenamiento $y_j \geq y_{j+1}$ y la inicialización con soluciones heurísticas (warm start) son esenciales para que solvers como Gurobi alcancen la optimalidad en instancias medianas.

El BPP tiene aplicaciones directas en logística (optimización de carga), manufactura (corte de materia prima) y asignación de recursos en la nube (bin packing de VMs).

---

## Problema 07 — Set Covering Problem (SCP)

**Referencia canónica:** Beasley, J. E. (1987). An algorithm for set covering problem. *European Journal of Operational Research*, 31(1), 85–93.

**Reseña:**

Beasley (1987) presenta uno de los algoritmos más influyentes para el SCP, combinando relajación Lagrangiana con subgradiente para obtener cotas duales ajustadas, seguido de una fase de búsqueda local para recuperar factibilidad primal. El artículo también introduce el conjunto de instancias de la OR-Library (incluyendo la clase `scp` con matrices de hasta 400×4000), que siguen siendo referencia obligatoria en la literatura.

La contribución central del trabajo es demostrar que la relajación Lagrangiana del SCP —obtenida al dualizar las restricciones de cobertura— produce cotas inferiores significativamente más ajustadas que la relajación LP estándar, con un costo computacional inferior al de resolver el LP completo en instancias grandes.

La instancia **50×200** (50 filas, 200 columnas) es de tamaño moderado y puede resolverse a optimalidad por un solver moderno como Gurobi en segundos. La estructura del SCP es más favorable que la del BPP para la relajación LP: la brecha de integralidad suele ser pequeña, lo que significa que la solución del LP relajado frecuentemente redondea a una solución entera factible de alta calidad.

El SCP aparece en múltiples contextos reales: localización de instalaciones de emergencia, diseño de rutas de vuelo (airline crew scheduling), selección de características en aprendizaje automático y diseño de redes de telecomunicaciones.
