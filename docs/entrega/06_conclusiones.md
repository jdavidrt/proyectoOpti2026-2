# Entregable 6 — Conclusiones

**Universidad Nacional de Colombia** | Optimización 2026-1
**Autores:** David Ramírez · Jaisson Machado Bautista

---

1. **Ambos modelos alcanzaron el óptimo certificado** (gap 0 %): Set Covering sobre la instancia completa 50×200 (costo 42, 9 columnas) y Bin Packing sobre 40 de 120 ítems (15 contenedores), con el interruptor listo para los 120 ítems al activar la licencia académica o WLS.

2. **La fortaleza de la relajación lineal explica todo el comportamiento computacional.** El SCP relaja a entero exacto (LP = IP = 42) y se cierra en un solo nodo; el BPP tiene una relajación débil (14.34 frente a 15) y depende del branch-and-bound. La misma teoría que se vio en clase se observó, medible, en los logs del solver.

3. **La ruptura de simetría `y_j ≥ y_{j+1}` fue decisiva** en el Bin Packing: sin ella, el solver exploraría las 15! permutaciones equivalentes de etiquetas de contenedores. Una desigualdad de modelado superó a la fuerza bruta.

4. **El análisis de sensibilidad reveló dos capas.** La estructural (contenedores ∝ 1/C, reducción del 52 % entre C=100 y C=200, con mesetas) y la computacional (picos de tiempo no monótonos en capacidades de frontera, hasta 75× la mediana). La dificultad del BPP vive en la aritmética pesos–capacidad, no en el tamaño.

5. **La interfaz importa.** El dashboard HTML autocontenido convirtió listas de índices en patrones legibles —barras de contenedores, matriz de cobertura, curva de sensibilidad— y mostró que, aun con la licencia gratuita de Gurobi, una capa visual delgada vuelve comunicable un resultado de optimización.

6. **Limitación honesta y su mitigación.** La licencia restringida (2000 variables) impidió correr el BPP completo localmente; se documentó el interruptor `ITEM_LIMIT`/WLS y se acotó el experimento a 40 ítems sin perder la validez metodológica. La cota teórica para 120 ítems (47, frente al óptimo conocido 48) queda anotada para verificación al desbloquear la licencia.

**Cierre.** El proyecto confirma, con dos problemas clásicos y un solver industrial, que en programación entera el modelado (formulación fuerte, simetría) pesa tanto como el algoritmo, y que reportar *cuánto cuesta* una solución es tan informativo como la solución misma.
