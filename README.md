# CS221 Final Project (Spring 2025) — Learning Heuristics for A* in Imperfect Mazes

This repository contains the code, data, and results for our final project in CS 221: Artificial Intelligence: Principles and Techniques. We explored how **tabular Q-learning** can be used to learn heuristics that improve the efficiency of A* search in imperfect mazes, which contain loops and misleading paths.

## Author Names: 
- Brooke Ballhaus  
- Riya Narain

---

## Repository Contents

| File / Folder               | Description |
|----------------------------|-------------|
| `CS221_Final_Project.ipynb` | Main Colab notebook with all code: data loading, training, evaluation, and visualization |
| `imperfect_maze.zip`       | Dataset of 1500 imperfect mazes (varying sizes, with loops) |
| `README.md`                | Overview of the project and how to reproduce it |

---

## Heuristics Compared

- `manhattan_heuristic`: Standard Manhattan distance
- `euclidean_heuristic`: Standard Euclidean distance
- `q_heuristic`: Heuristic derived from Q-learning (negative of max Q-value per state to approximate cost-to-go)

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
results_df = run_hyperparameter_search(train_mazes, n_maps=300, n_trials_per_map=30)

# Train and evaluate
Q = train_q_learning_reversed(
    maze, goal, actions,
    discount=best_config["discount"],
    explorationProb=best_config["explorationProb"],
    step_size=best_config["step_size"],
    num_sample_starts=best_config["num_sample_starts"],
    step_multiplier=best_config["step_multiplier"]
)
heuristics = {
        "Manhattan": manhattan_heuristic,
        "Euclidean": euclidean_heuristic,
        "Q-learned": q_heuristic
    }
