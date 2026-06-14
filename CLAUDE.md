# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Academic optimization project (Universidad Nacional de Colombia, course Optimización 2026-1) covering two combinatorial
problems solved with Gurobi ILP models:

- **Bin Packing Problem (BPP)** — `models/bin_packing.py`, instance `data/BinPacking_u120_01.txt` (120 items, capacity 150)
- **Set Covering Problem (SCP)** — `models/set_covering.py`, instance `data/SetCovering_50x200.txt` (50 rows, 200 columns)

Deliverable due **2026-06-15**. Checklist of required deliverables (formulations, literature reviews, sensitivity
analysis, conclusions, AI usage log, etc.) is in `GUIA_PROYECTO_OPTI_ClaudeCode.md`.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Requires a Gurobi 11+ license (academic license via `grbgetkey`).

## Running the models

```powershell
# Bin Packing model — reads data/BinPacking_u120_01.txt, writes results/bin_packing_solution.txt
python models/bin_packing.py

# Set Covering model — reads data/SetCovering_50x200.txt, writes results/set_covering_solution.txt
python models/set_covering.py

# Sensitivity analysis on bin capacity (varies C from 100 to 200, step 10) — takes several minutes
# Writes results/sensitivity_capacity.png and results/sensitivity_summary.csv
python sensitivity/sensitivity_analysis.py
```

There are no automated tests, build, or lint commands — correctness is verified by running the solver scripts and
inspecting console output / files written to `results/`.

## Architecture

- **`models/bin_packing.py`** and **`models/set_covering.py`** each follow the same pattern: a `load_*` function
  parses the OR-Library format instance file into plain Python data structures, and a `solve_*` function builds the
  Gurobi model, solves it (5-minute `TimeLimit`), prints a summary (status, objective, MIP gap, solve time), and
  writes a human-readable solution report to `results/`.
- **`sensitivity/sensitivity_analysis.py`** imports `load_bin_packing` directly from `models/bin_packing.py` (via
  `sys.path` manipulation) and re-implements the BPP model as `solve_bpp_with_capacity(n, w, C, time_limit)` so the
  bin capacity `C` can be swept as a parameter (100–200, step 10). Each run produces a result dict
  (`bins_used`, `solve_time`, `gap`, `status`). Results are aggregated into a 3-panel matplotlib figure
  (`results/sensitivity_capacity.png`) and a CSV summary (`results/sensitivity_summary.csv`).
- All scripts resolve paths relative to the project root via
  `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`, so they can be run from any working directory.
- Data files use OR-Library formats:
  - BPP: line 1 = number of test cases; per case, header line `n_items capacity optimal`, then `n_items` weight values.
  - SCP: `m n` (rows, columns), then `n` column costs, then for each row a count `k` followed by `k` 1-based column
    indices (converted to 0-based on load).

## AI usage logging (`bitacora_ia.md`)

Course policy requires every AI-assisted interaction (including Claude Code) to be logged in `bitacora_ia.md`, with
date, tool, task, prompt used, result, human verification status, and an estimated percentage of the total
deliverable. Total AI usage across the project must stay **under 20%**. When making substantive changes on behalf of
the user for this deliverable, add an entry to `bitacora_ia.md` following the existing template.
