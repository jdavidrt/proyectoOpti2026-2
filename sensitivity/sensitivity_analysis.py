"""
Sensitivity Analysis — Bin Packing Problem
==========================================
Varies bin capacity C from 100 to 200 (step 10).
For each value of C:
  - Solves the BPP ILP
  - Records bins used, solve time, and MIP gap
Saves plot: results/sensitivity_capacity.png
"""

import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB

# Allow importing the data loader from models/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))
from bin_packing import load_bin_packing


# ---------------------------------------------------------------------------
# Parametric solve (capacity as free parameter)
# ---------------------------------------------------------------------------

def solve_bpp_with_capacity(n: int, w: list[int], C: int, time_limit: int = 120) -> dict:
    """Solve BPP for a given capacity C. Returns result dict."""
    J = list(range(n))
    I = list(range(n))

    model = gp.Model("BPP_sensitivity")
    model.Params.LogToConsole = 0
    model.Params.TimeLimit = time_limit

    x = model.addVars(I, J, vtype=GRB.BINARY, name="x")
    y = model.addVars(J, vtype=GRB.BINARY, name="y")

    model.setObjective(gp.quicksum(y[j] for j in J), GRB.MINIMIZE)

    # Each item in exactly one bin
    model.addConstrs(
        (gp.quicksum(x[i, j] for j in J) == 1 for i in I),
        name="assign"
    )

    # Capacity + linking: sum_i w[i]*x[i,j] <= C*y[j]
    model.addConstrs(
        (gp.quicksum(w[i] * x[i, j] for i in I) <= C * y[j] for j in J),
        name="capacity"
    )

    # Symmetry breaking
    model.addConstrs(
        (y[j] >= y[j + 1] for j in range(n - 1)),
        name="symmetry"
    )

    t0 = time.time()
    model.optimize()
    elapsed = time.time() - t0

    status = model.Status
    bins_used = int(round(model.ObjVal)) if status in (GRB.OPTIMAL, GRB.SUBOPTIMAL, GRB.TIME_LIMIT) else None
    gap = model.MIPGap if status not in (GRB.INFEASIBLE, GRB.INF_OR_UNBD) else None

    return {
        "C": C,
        "bins_used": bins_used,
        "solve_time": elapsed,
        "gap": gap,
        "status": status,
    }


# ---------------------------------------------------------------------------
# Main sensitivity loop
# ---------------------------------------------------------------------------

def run_sensitivity(data_path: str, results_dir: str, item_limit: int | None = None) -> None:
    n, _C0, w = load_bin_packing(data_path)
    n_full = n

    # --- TRIAL-LICENSE REDUCTION (mirrors models/bin_packing.py) -------------
    # The trial / pip Gurobi license caps the model at ~2000 variables. Each
    # capacity solve builds n*n + n binary vars, so under the trial license we
    # sweep a reduced subset of items. Pass item_limit=None (academic license)
    # to sweep the complete 120-item instance.
    trial_mode = item_limit is not None and item_limit < n
    if trial_mode:
        n = item_limit
        w = w[:n]
        print(f"[TRIAL MODE] Reduced instance: {n} of {n_full} items")
    print(f"Loaded instance: {n} items")

    capacities = list(range(100, 201, 10))
    results = []

    for C in capacities:
        print(f"  Solving C={C} ...", end=" ", flush=True)
        res = solve_bpp_with_capacity(n, w, C)
        results.append(res)
        print(f"bins={res['bins_used']}  time={res['solve_time']:.2f}s  gap={res['gap']:.2%}" if res["gap"] is not None else f"bins={res['bins_used']}  time={res['solve_time']:.2f}s")

    # --- Extract series ---
    caps       = [r["C"]          for r in results]
    bins_list  = [r["bins_used"]  for r in results]
    times      = [r["solve_time"] for r in results]
    gaps       = [r["gap"] * 100 if r["gap"] is not None else 0.0 for r in results]

    # --- Plot ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    title = "Bin Packing — Sensitivity Analysis: Bin Capacity"
    if trial_mode:
        title += f"  (TRIAL license: {n} of {n_full} items)"
    fig.suptitle(title, fontsize=14)

    # Subplot 1: bins used vs capacity
    axes[0].plot(caps, bins_list, marker="o", color="steelblue", linewidth=2)
    axes[0].set_xlabel("Bin Capacity (C)")
    axes[0].set_ylabel("Number of Bins Used")
    axes[0].set_title("Bins Used vs Capacity")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    for cx, bx in zip(caps, bins_list):
        if bx is not None:
            axes[0].annotate(str(bx), (cx, bx), textcoords="offset points", xytext=(0, 6), fontsize=7, ha="center")

    # Subplot 2: solve time vs capacity
    axes[1].bar(caps, times, color="darkorange", width=7)
    axes[1].set_xlabel("Bin Capacity (C)")
    axes[1].set_ylabel("Solve Time (s)")
    axes[1].set_title("Solve Time vs Capacity")
    axes[1].grid(True, axis="y", linestyle="--", alpha=0.6)

    # Subplot 3: MIP gap vs capacity
    axes[2].plot(caps, gaps, marker="s", color="firebrick", linewidth=2)
    axes[2].set_xlabel("Bin Capacity (C)")
    axes[2].set_ylabel("MIP Gap (%)")
    axes[2].set_title("MIP Gap vs Capacity")
    axes[2].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    os.makedirs(results_dir, exist_ok=True)
    plot_path = os.path.join(results_dir, "sensitivity_capacity.png")
    plt.savefig(plot_path, dpi=150)
    print(f"\nPlot saved to: {plot_path}")

    # --- Save CSV summary ---
    csv_path = os.path.join(results_dir, "sensitivity_summary.csv")
    with open(csv_path, "w") as f:
        f.write("capacity,bins_used,solve_time_s,mip_gap_pct\n")
        for r in results:
            gap_str = f"{r['gap']*100:.4f}" if r["gap"] is not None else ""
            f.write(f"{r['C']},{r['bins_used']},{r['solve_time']:.4f},{gap_str}\n")
    print(f"Summary CSV saved to: {csv_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path   = os.path.join(base, "data",    "BinPacking_u120_01.txt")
    results_dir = os.path.join(base, "results")

    # ============================ LICENSE SWITCH ============================
    # Same constraint as models/bin_packing.py: the trial / pip Gurobi license
    # is limited to ~2000 vars, so we sweep a reduced item subset for now.
    #
    #   TRIAL license    ->  ITEM_LIMIT = 40    (40*40 + 40 = 1,640 vars < 2000)
    #   ACADEMIC license ->  ITEM_LIMIT = None  (full 120-item instance)
    #
    # TODO(2026-06-15): set `ITEM_LIMIT = None` after activating the academic
    # license to run the full sensitivity sweep.
    # ========================================================================
    ITEM_LIMIT = 40

    run_sensitivity(data_path, results_dir, item_limit=ITEM_LIMIT)
