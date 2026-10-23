# AGENTS.md

## Summary
Stanford CS 221 (Spring 2025) final project by Brooke Ballhaus and Riya Narain.
Tabular Q-learning is trained backward from the goal to learn a cost-to-go
heuristic for A* search, which is compared against Manhattan and Euclidean
heuristics on 1500 "imperfect" mazes (mazes with loops and misleading paths).
All code lives in a single Google Colab notebook.

## Files
- `CS221_Final_Project.ipynb` - the whole pipeline: loading, Q-learning, A*, tuning, evaluation, plots.
- `imperfect_maze.zip` - dataset: `imperfect_maze/mazeN_dimD.txt` (1500 mazes; also contains `__MACOSX/` entries).
- `requirements.txt` - third-party packages (all preinstalled on Colab).
- `README.md` - project overview and reproduction steps.
- `tests/test_notebook.py` - pytest smoke tests (no notebook execution; see Tests).
- `.github/workflows/tests.yml` - CI: runs `python -m pytest -q` on Python 3.11 for pushes/PRs to `main`.

## Setup
- Colab (intended): open the notebook, run cell 1, and upload `imperfect_maze.zip` when prompted.
  The cell extracts it into `imperfect_maze/` and reads from `input_dir = "imperfect_maze/imperfect_maze"`.
- Local Jupyter: `pip install -r requirements.txt` plus `jupyter`. Then:
  - `unzip imperfect_maze.zip -d imperfect_maze` from the notebook's working directory, so files land in `imperfect_maze/imperfect_maze/*.txt`.
  - Replace `from google.colab import files`, `files.upload()` (cells 1 and 22) and `files.download(...)` (cells 15 and 21) with local paths.

## How to run
Run cells top to bottom. Cell indices below are 0-based code-cell positions in the notebook JSON.
1. Cell 0: imports (including scikit-learn, seaborn, and `IPython.display.display`). Cell 1: upload/unzip dataset, list maze files.
2. Cell 2: `split_mazes(maze_files, train_frac=0.2, seed=42)` -> `train_mazes`, `test_mazes`.
3. Cell 11: `run_hyperparameter_search(train_mazes, n_maps=30, n_trials_per_map=30)` -> `hyperparameter_results.csv/json`
   (slow; the README example shows `n_maps=300`).
4. Cell 12: evaluates each heuristic on `test_mazes` with a hardcoded `best_config` -> `final_heuristic_comparison.csv/json`.
5. Cells 13-23: visualizations, parameter-importance heatmap, per-dimension summaries, downloads.

## Tests
- `pip install pytest && python -m pytest -q` (runs in well under a second; no numpy/pandas needed).
- The tests never execute the notebook. They check it is valid JSON, that every code cell compiles
  (with `google.colab` imports, `files.upload()`/`files.download()` calls and `!`/`%` lines neutralized),
  that every name read anywhere is a builtin, imported, or defined in some cell, and that
  `imperfect_maze.zip` contains files under `imperfect_maze/`.
- When adding cells that use a new library, add its import to cell 0 (and the package to
  `requirements.txt`), or the undefined-name test fails.

## Key functions (cell)
- `split_mazes` (2), `load_maze` (3) - maze I/O; a maze is a numpy grid where 0 = free cell.
- `q_heuristic`, `manhattan_heuristic`, `euclidean_heuristic` (4) - heuristics; `q_heuristic` reads a global `Q`.
- `TabularQLearning` (5) - Q-table agent (`getQ`, `choose_action`, `update`).
- `astar(maze, start, goal, heuristic)` (6) - returns `(came_from, cost)`; nodes expanded = `len(cost)`.
- `train_q_learning_reversed` (7) - trains Q from the goal outward.
- `evaluate_runtime` (8), `run_single_map_search` (9), `run_hyperparameter_search` (10) - tuning.
- `visualize_heuristics_on_sampled_paths` (13), `plot_runtime_progression` (14) - plots.
- Actions are always `[(0, 1), (0, -1), (1, 0), (-1, 0)]`.

## Guardrails
- `imperfect_maze.zip` is the canonical dataset. Do not modify, regenerate, or re-zip it; do not commit the extracted folder.
- The notebook's results are the reported project results. Do not change `best_config`,
  the split seed, or experiment logic without being asked; add new cells instead of rewriting existing ones.
- Do not commit generated CSV/JSON/PNG outputs unless asked.
- Edit the notebook as JSON carefully (preserve cell order and metadata); do not run it unless asked - tuning is expensive.
- The saved notebook currently has no stored cell outputs; reported numbers come from the CSVs produced when it is run.
