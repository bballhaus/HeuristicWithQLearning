# CS221 Final Project — Learning Heuristics for A* in Imperfect Mazes

This repository contains the code, data, and results for our final project in CS 221. We explored using **tabular Q-learning** to learn heuristics that improve A* search efficiency in imperfect mazes.

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
train_mazes, val_mazes, test_mazes = split_mazes_three_way(maze_files)

# Tune Q-learning
tuned_results = tune_qlearning_hyperparams(train_mazes, score_weights=(1.0, 1.0, 0.2))

# Train and evaluate
Q = train_q_learning(maze, goal, goal, actions, ...)
heuristics = [("manhattan", manhattan), ("euclidean", euclidean), ("qlearned", learned_heuristic(Q, actions))]
