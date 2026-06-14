"""
Set Covering Problem (SCP) — Gurobi ILP Model
=============================================
Formulation:
    min  sum_j  c[j] * x[j]
    s.t. sum_{j: j covers i}  x[j]  >= 1    for all i   (every row covered)
         x[j] in {0, 1}

Instance: OR-Library format  data/SetCovering_50x200.txt
Output:   results/set_covering_solution.txt
"""

import time
import os
import gurobipy as gp
from gurobipy import GRB


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_set_covering(filepath: str) -> tuple[int, int, list[int], list[list[int]]]:
    """
    Parse OR-Library SCP file.
    Returns (m_rows, n_cols, costs, coverage)
      costs    : list of column costs, length n_cols
      coverage : coverage[i] = list of column indices (0-based) that cover row i
    """
    with open(filepath) as f:
        tokens = f.read().split()

    idx = 0
    m = int(tokens[idx]); idx += 1     # number of rows
    n = int(tokens[idx]); idx += 1     # number of columns

    # Column costs
    costs = [int(tokens[idx + j]) for j in range(n)]
    idx += n

    # Row coverage: for each row i, read k then k column indices
    coverage = []
    for i in range(m):
        k = int(tokens[idx]); idx += 1
        cols = [int(tokens[idx + t]) - 1 for t in range(k)]  # convert to 0-based
        idx += k
        coverage.append(cols)

    return m, n, costs, coverage


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def solve_set_covering(data_path: str, results_path: str) -> None:
    m, n, costs, coverage = load_set_covering(data_path)
    print(f"Instance: {m} rows, {n} columns")

    I = list(range(m))
    J = list(range(n))

    model = gp.Model("SetCovering")
    model.Params.LogToConsole = 1
    model.Params.TimeLimit = 300

    # --- Decision variables ---
    # x[j] = 1 if column j is selected in the cover
    x = model.addVars(J, vtype=GRB.BINARY, name="x")

    # --- Objective: minimize total cost of selected columns ---
    # min sum_{j in J} c[j] * x[j]
    model.setObjective(gp.quicksum(costs[j] * x[j] for j in J), GRB.MINIMIZE)

    # --- Constraint: every row i must be covered by at least one selected column ---
    # sum_{j in A[i]} x[j] >= 1   for all i in I
    # where A[i] is the set of columns that cover row i
    model.addConstrs(
        (gp.quicksum(x[j] for j in coverage[i]) >= 1 for i in I),
        name="cover"
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

    obj_val = model.ObjVal if status in (GRB.OPTIMAL, GRB.SUBOPTIMAL, GRB.TIME_LIMIT) else None
    gap     = model.MIPGap if status != GRB.INFEASIBLE else None
    selected = [j for j in J if x[j].X > 0.5] if obj_val is not None else []

    print(f"\n{'='*50}")
    print(f"Status           : {status_str}")
    print(f"Total cost       : {obj_val:.2f}" if obj_val else "Total cost       : N/A")
    print(f"Columns selected : {len(selected)}")
    print(f"MIP gap          : {gap:.4%}" if gap is not None else "MIP gap          : N/A")
    print(f"Solve time       : {elapsed:.2f}s")
    print(f"{'='*50}\n")

    # --- Save results ---
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        f.write("Set Covering Solution\n")
        f.write(f"{'='*40}\n")
        f.write(f"Instance         : {data_path}\n")
        f.write(f"Rows             : {m}\n")
        f.write(f"Columns          : {n}\n")
        f.write(f"Status           : {status_str}\n")
        f.write(f"Total cost       : {obj_val:.2f}\n" if obj_val else "Total cost       : N/A\n")
        f.write(f"Columns selected : {len(selected)}\n")
        f.write(f"MIP gap          : {gap:.4%}\n" if gap is not None else "MIP gap          : N/A\n")
        f.write(f"Solve time       : {elapsed:.2f}s\n\n")
        f.write(f"Selected columns (0-indexed): {selected}\n")

    print(f"Results saved to: {results_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path    = os.path.join(base, "data",    "SetCovering_50x200.txt")
    results_path = os.path.join(base, "results", "set_covering_solution.txt")
    solve_set_covering(data_path, results_path)
