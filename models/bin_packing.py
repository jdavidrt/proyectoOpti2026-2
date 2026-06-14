"""
Bin Packing Problem (BPP) — Gurobi ILP Model
=============================================
Formulation:
    min  sum_j  y[j]
    s.t. sum_j  x[i][j]  = 1          for all i   (each item in exactly one bin)
         sum_i  w[i]*x[i][j] <= C*y[j] for all j   (capacity + linking constraint)
         x[i][j] in {0,1}, y[j] in {0,1}

Instance: OR-Library format  data/BinPacking_u120_01.txt
Output:   results/bin_packing_solution.txt
"""

import time
import os
import gurobipy as gp
from gurobipy import GRB


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_bin_packing(filepath: str) -> tuple[int, int, list[int]]:
    """Parse OR-Library bin packing file. Returns (n_items, capacity, weights)."""
    with open(filepath) as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    idx = 0
    _n_cases = int(lines[idx]); idx += 1          # number of test cases (we use the first)
    header = lines[idx].split(); idx += 1
    n_items, capacity, _opt = int(header[0]), int(header[1]), int(header[2])
    weights = [int(lines[idx + k]) for k in range(n_items)]
    return n_items, capacity, weights


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def solve_bin_packing(data_path: str, results_path: str) -> None:
    n, C, w = load_bin_packing(data_path)
    print(f"Instance: {n} items, bin capacity = {C}")

    # Upper bound on bins needed: n (one item per bin)
    J = list(range(n))
    I = list(range(n))

    model = gp.Model("BinPacking")
    model.Params.LogToConsole = 1
    model.Params.TimeLimit = 300   # 5-minute safety limit

    # --- Decision variables ---
    # x[i,j] = 1 if item i is assigned to bin j
    x = model.addVars(I, J, vtype=GRB.BINARY, name="x")
    # y[j] = 1 if bin j is used
    y = model.addVars(J, vtype=GRB.BINARY, name="y")

    # --- Objective: minimize number of bins used ---
    model.setObjective(gp.quicksum(y[j] for j in J), GRB.MINIMIZE)

    # --- Constraint 1: each item assigned to exactly one bin ---
    # sum_{j} x[i,j] = 1   for all i in I
    model.addConstrs(
        (gp.quicksum(x[i, j] for j in J) == 1 for i in I),
        name="assign"
    )

    # --- Constraint 2: bin capacity + linking constraint ---
    # sum_{i} w[i] * x[i,j] <= C * y[j]   for all j in J
    # This simultaneously enforces capacity and links x to y:
    # if y[j]=0 then no item can be placed in bin j.
    model.addConstrs(
        (gp.quicksum(w[i] * x[i, j] for i in I) <= C * y[j] for j in J),
        name="capacity"
    )

    # --- Symmetry-breaking: bins ordered by index ---
    # y[j] >= y[j+1]  reduces equivalent permutations of bin labels
    model.addConstrs(
        (y[j] >= y[j + 1] for j in range(n - 1)),
        name="symmetry"
    )

    # --- Solve ---
    t0 = time.time()
    model.optimize()
    elapsed = time.time() - t0

    # --- Report ---
    status = model.Status
    status_map = {GRB.OPTIMAL: "OPTIMAL", GRB.SUBOPTIMAL: "SUBOPTIMAL",
                  GRB.INFEASIBLE: "INFEASIBLE", GRB.TIME_LIMIT: "TIME_LIMIT"}
    status_str = status_map.get(status, f"STATUS_{status}")

    bins_used = int(round(model.ObjVal)) if status in (GRB.OPTIMAL, GRB.SUBOPTIMAL, GRB.TIME_LIMIT) else None
    gap = model.MIPGap if status != GRB.INFEASIBLE else None

    print(f"\n{'='*50}")
    print(f"Status       : {status_str}")
    print(f"Bins used    : {bins_used}")
    print(f"MIP gap      : {gap:.4%}" if gap is not None else "MIP gap      : N/A")
    print(f"Solve time   : {elapsed:.2f}s")
    print(f"{'='*50}\n")

    # --- Save results ---
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        f.write(f"Bin Packing Solution\n")
        f.write(f"{'='*40}\n")
        f.write(f"Instance     : {data_path}\n")
        f.write(f"Items        : {n}\n")
        f.write(f"Capacity     : {C}\n")
        f.write(f"Status       : {status_str}\n")
        f.write(f"Bins used    : {bins_used}\n")
        f.write(f"MIP gap      : {gap:.4%}\n" if gap is not None else "MIP gap      : N/A\n")
        f.write(f"Solve time   : {elapsed:.2f}s\n\n")

        if status in (GRB.OPTIMAL, GRB.SUBOPTIMAL):
            f.write("Bin assignments:\n")
            for j in J:
                if y[j].X > 0.5:
                    items_in_bin = [i for i in I if x[i, j].X > 0.5]
                    load = sum(w[i] for i in items_in_bin)
                    f.write(f"  Bin {j:3d}: items={items_in_bin}, load={load}/{C}\n")

    print(f"Results saved to: {results_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path    = os.path.join(base, "data",    "BinPacking_u120_01.txt")
    results_path = os.path.join(base, "results", "bin_packing_solution.txt")
    solve_bin_packing(data_path, results_path)
