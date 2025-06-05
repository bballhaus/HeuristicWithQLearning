# CS221 Final Project (Spring 2025) — Learning Heuristics for A* in Imperfect Mazes

This repository contains the code, data, and results for our final project in CS 221. We explored using **tabular Q-learning** to learn heuristics that improve A* search efficiency in imperfect mazes.

## Author Names: 
- Brooke Ballhaus  
- Riya Narain

---

## Repository Contents

| File / Folder               | Description |
|----------------------------|-------------|
| `CS221_Final_Project.ipynb` | Main Colab notebook with all code: data loading, training, evaluation, and visualization |
| `imperfect_maze.zip`       | Dataset of 1500 imperfect mazes (varying sizes, with loops) |
| `tuning_results.csv`       | Output of grid search for Q-learning hyperparameters |
| `final_evaluation.csv`     | Evaluation results on test mazes for all heuristics |
| `README.md`                | Overview of the project and how to reproduce it |

---

## Heuristics Compared

- `manhattan`: Standard Manhattan distance
- `euclidean`: Standard Euclidean distance
- `qlearned`: Heuristic learned using Q-learning value estimates (converted to cost-to-go)

---

## How to Reproduce Results

### Step-by-step in Google Colab:

1. Upload `CS221_Final_Project.ipynb` and `imperfect_maze.zip`
2. Run all notebook cells in order.
   - Mazes are loaded and split into train/test.
   - Q-learning is trained using hyperparameters found via tuning.
   - A* is run using each heuristic and results are saved.

### Main functions called:

```python
# Load and split mazes
maze_files = [os.path.join(input_dir, f) for f in sorted(os.listdir(input_dir)) if f.endswith(".txt")]
train_mazes, test_mazes = split_mazes(maze_files)

# Tune Q-learning
results_df = run_hyperparameter_search(maze_files, n_maps=30, n_trials_per_map=30)

# Train and evaluate
Q = train_q_learning_reversed(
    maze, goal, actions,
    discount=best_config["discount"],
    explorationProb=best_config["explorationProb"],
    step_size=best_config["step_size"],
    num_sample_starts=best_config["num_sample_starts"],
    step_multiplier=best_config["step_multiplier"]
)
heuristics = [("manhattan", manhattan), ("euclidean", euclidean), ("qlearned", learned_heuristic(Q, actions))]
