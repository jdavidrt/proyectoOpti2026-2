"""
build_dashboard.py - Dashboard generator for the BPP / SCP optimization project
===============================================================================
Bakes a single self-contained `dashboard.html` (no server, no internet) from:
  - the instance files in   data/
  - the solver outputs in   results/

Live solve + fallback (default):
  Before reading the result files, this script tries to RE-SOLVE the models
  with Gurobi. If a full (academic) license is active it solves the complete
  120-item Bin Packing instance; if only the size-limited trial license is
  available it falls back to the reduced 40-item run; if Gurobi or its license
  is unavailable it simply reuses whatever is already saved in results/.

Usage (from the project root, with the venv active):
    python dashboard/build_dashboard.py            # live solve, then build
    python dashboard/build_dashboard.py --no-solve # just rebuild from saved results

Output: dashboard/dashboard.html  (double-click to open)
"""

import os
import re
import sys
import csv
import json
import argparse
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")
RES_DIR = os.path.join(BASE, "results")
MODELS_DIR = os.path.join(BASE, "models")
SENS_DIR = os.path.join(BASE, "sensitivity")
HERE = os.path.dirname(os.path.abspath(__file__))

BPP_DATA = os.path.join(DATA_DIR, "BinPacking_u120_01.txt")
SCP_DATA = os.path.join(DATA_DIR, "SetCovering_50x200.txt")
BPP_RES = os.path.join(RES_DIR, "bin_packing_solution.txt")
SCP_RES = os.path.join(RES_DIR, "set_covering_solution.txt")
SENS_CSV = os.path.join(RES_DIR, "sensitivity_summary.csv")


# ---------------------------------------------------------------------------
# Instance-file parsers (stdlib only -- no gurobipy import needed to build)
# ---------------------------------------------------------------------------

def parse_bpp_data(path):
    """Returns (n_items, capacity, weights) from an OR-Library BPP file."""
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    idx = 1                                   # line 0 = number of test cases
    header = lines[idx].split(); idx += 1
    n, cap = int(header[0]), int(header[1])
    weights = [int(lines[idx + k]) for k in range(n)]
    return n, cap, weights


def parse_scp_data(path):
    """Returns (m_rows, n_cols, costs, coverage) from an OR-Library SCP file."""
    with open(path) as f:
        tok = f.read().split()
    i = 0
    m = int(tok[i]); i += 1
    n = int(tok[i]); i += 1
    costs = [int(tok[i + j]) for j in range(n)]; i += n
    coverage = []
    for _ in range(m):
        k = int(tok[i]); i += 1
        cols = [int(tok[i + t]) - 1 for t in range(k)]; i += k   # to 0-based
        coverage.append(cols)
    return m, n, costs, coverage


# ---------------------------------------------------------------------------
# Result-file parsers
# ---------------------------------------------------------------------------

def _grab(pattern, text, cast=str, default=None):
    mt = re.search(pattern, text)
    if not mt:
        return default
    try:
        return cast(mt.group(1))
    except (ValueError, TypeError):
        return default


def parse_bpp_results(path):
    if not os.path.exists(path):
        return {}
    txt = open(path, encoding="utf-8", errors="replace").read()
    out = {
        "status": _grab(r"Status\s*:\s*(\S+)", txt),
        "bins_used": _grab(r"Bins used\s*:\s*(\d+)", txt, int),
        "items_solved": _grab(r"Items\s*:\s*(\d+)", txt, int),
        "capacity": _grab(r"Capacity\s*:\s*(\d+)", txt, int),
        "gap": _grab(r"MIP gap\s*:\s*([\d.]+)%", txt, float),
        "solve_time": _grab(r"Solve time\s*:\s*([\d.]+)s", txt, float),
        "license_mode": _grab(r"License mode\s*:\s*([A-Za-z]+)", txt),
    }
    bins = []
    for mt in re.finditer(r"Bin\s+(\d+)\s*:\s*items=\[(.*?)\],\s*load=(\d+)/(\d+)", txt):
        items_raw = mt.group(2).strip()
        items = [int(x) for x in items_raw.split(",") if x.strip() != ""] if items_raw else []
        bins.append({"id": int(mt.group(1)), "items": items,
                     "load": int(mt.group(3)), "cap": int(mt.group(4))})
    out["bins"] = bins
    return out


def parse_scp_results(path):
    if not os.path.exists(path):
        return {}
    txt = open(path, encoding="utf-8", errors="replace").read()
    sel_raw = _grab(r"Selected columns.*?:\s*\[(.*?)\]", txt, str, "")
    selected = [int(x) for x in sel_raw.split(",") if x.strip() != ""] if sel_raw else []
    return {
        "status": _grab(r"Status\s*:\s*(\S+)", txt),
        "total_cost": _grab(r"Total cost\s*:\s*([\d.]+)", txt, float),
        "num_selected": _grab(r"Columns selected\s*:\s*(\d+)", txt, int),
        "gap": _grab(r"MIP gap\s*:\s*([\d.]+)%", txt, float),
        "solve_time": _grab(r"Solve time\s*:\s*([\d.]+)s", txt, float),
        "selected": selected,
    }


def parse_sensitivity(path):
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
                "capacity": int(float(r["capacity"])),
                "bins_used": int(float(r["bins_used"])),
                "solve_time_s": float(r["solve_time_s"]),
                "mip_gap_pct": float(r["mip_gap_pct"]),
            })
    return rows


# ---------------------------------------------------------------------------
# Live solve (best effort, with graceful fallback)
# ---------------------------------------------------------------------------

def solve_live():
    """Try to refresh results via Gurobi. Returns (source, log[])."""
    log = []
    solved_any = False
    sys.path.insert(0, MODELS_DIR)

    # Set Covering -- fits any license.
    try:
        from set_covering import solve_set_covering
        solve_set_covering(SCP_DATA, SCP_RES)
        log.append("SCP: solved live (full 50x200 instance).")
        solved_any = True
    except Exception as e:
        log.append("SCP: live solve unavailable (%s) -> using saved results." % type(e).__name__)

    # Bin Packing -- try full instance first, fall back to reduced.
    try:
        from bin_packing import solve_bin_packing
        try:
            solve_bin_packing(BPP_DATA, BPP_RES, item_limit=None)
            log.append("BPP: solved live (full 120-item instance, academic license).")
        except Exception:
            solve_bin_packing(BPP_DATA, BPP_RES, item_limit=40)
            log.append("BPP: full instance exceeded license -> solved reduced 40-item run (trial).")
        solved_any = True
    except Exception as e:
        log.append("BPP: live solve unavailable (%s) -> using saved results." % type(e).__name__)

    return ("live" if solved_any else "saved"), log


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build(do_solve=True):
    source, log = ("saved", ["--no-solve: built from saved result files."])
    if do_solve:
        source, log = solve_live()

    # Source data
    bpp_n, bpp_cap, bpp_w = parse_bpp_data(BPP_DATA)
    scp_m, scp_n, scp_costs, scp_cov = parse_scp_data(SCP_DATA)

    # Solver outputs
    bpp = parse_bpp_results(BPP_RES)
    scp = parse_scp_results(SCP_RES)
    sens = parse_sensitivity(SENS_CSV)

    bpp.update({"n_full": bpp_n, "weights": bpp_w,
                "capacity": bpp.get("capacity") or bpp_cap})
    scp.update({"m": scp_m, "n": scp_n, "costs": scp_costs, "coverage": scp_cov})

    license_mode = bpp.get("license_mode") or "unknown"

    data = {
        "meta": {
            "generated": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "source": source,
            "license_mode": license_mode,
            "solve_log": log,
        },
        "bpp": bpp,
        "scp": scp,
        "sens": sens,
    }

    template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    html = template.replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))
    out_path = os.path.join(HERE, "dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Source        :", source)
    for line in log:
        print("  -", line)
    print("BPP bins      :", len(bpp.get("bins", [])),
          "| SCP columns  :", len(scp.get("selected", [])),
          "| sensitivity pts:", len(sens))
    print("Dashboard ->", out_path)
    return out_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the optimization dashboard.")
    ap.add_argument("--no-solve", dest="solve", action="store_false",
                    help="skip live solving; build from saved result files only")
    ap.set_defaults(solve=True)
    args = ap.parse_args()
    build(do_solve=args.solve)
