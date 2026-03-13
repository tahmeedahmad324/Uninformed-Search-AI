# Uninformed-Search-AI

A Python-based maze solver utilizing multiple un(in)formed search algorithms (BFS, DFS, UCS, DLS, IDDFS, Bidirectional Search) with grid visualization using Matplotlib.

## Overview

This repository contains a Python implementation of various uninformed search algorithms used to navigate and solve a grid-based maze. The project also features a built-in visualization using `matplotlib` to render the exploration order and the final grid state.

*(Note: The term "uniformed search" is commonly known in AI as "uninformed" or "blind" search.)*

## Features

The `MazeSolver` class supports:

- **BFS** (Breadth-First Search)
- **DFS** (Depth-First Search)
- **UCS** (Uniform Cost Search)
- **DLS** (Depth-Limited Search)
- **IDDFS** (Iterative Deepening Depth-First Search)
- **Bidirectional Search**

## Grid Legend

- `S`: Start position
- `T`: Target position
- `-1`: Obstacles / Walls
- `0`: Open unvisited path
- `1, 2, 3...`: Visited/exploration order

## Requirements

```bash
pip install matplotlib numpy
```

## How to Run

```bash
# Clone
git clone https://github.com/tahmeedahmad324/Uninformed-Search-AI.git
cd Uninformed-Search-AI

# Run
python maze_solver.py
```

## Switching Algorithms

Edit `algorithm_choice` at the bottom of `maze_solver.py`:

```python
algorithm_choice = "DFS"  # Options: BFS, DFS, UCS, DLS, IDDFS, BIDIRECTIONAL
```

## Notes

- The neighbor expansion order includes diagonals and is clockwise as implemented in `get_adjacent_cells`.
- Obstacles are represented by the string `"-1"` in the grid.
