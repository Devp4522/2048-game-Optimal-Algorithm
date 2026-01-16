# 2048 Solver – Quant Club

**Author:** Dev Patel
**Project Type:** Game Simulation + Algorithmic Strategy
**Goal:** Reach the *2048 tile* in the **minimum number of moves** using an intelligent Python-based algorithm.

This repository contains:

* A **manual (playable) implementation** of the 2048 game
* An **automated solver** that plays the game using a custom strategy
* Experiments comparing performance across runs

The project is built as both a *codebase* and a *report*, with explanations embedded directly in the notebook and source files.

---

## 🧩 Problem Statement

2048 is played on a 4×4 grid where tiles slide in four directions: **Up, Down, Left, Right**.

Rules:

* Tiles with the same value merge into one with double the value.
* After every valid move, a new tile (2 or 4) spawns at a random empty position.
* A move is invalid if it does not change the board.
* The game is **won** when a tile reaches **2048**.
* The game is **lost** when no valid moves remain.

The objective is to **design an algorithm that reaches 2048 in the fewest moves possible**.

---

## 🛠️ What’s Implemented

1. **Manual Game Engine**

   * Fully playable version of 2048 (CLI-based)
   * Implements:

     * Tile movement
     * Merging logic
     * Random tile generation
     * Win & lose detection

2. **Automated Solver**

   * Simulates the game internally
   * Chooses moves based on heuristics
   * Aims to minimize total moves to reach 2048

3. **Strategy Design**

The solver is based on principles commonly used in strong 2048 agents:

* Board structure preservation (keeping high tiles in a corner)
* Merge prioritization
* Penalizing chaotic board states
* Rewarding monotonic rows/columns
* Maximizing empty spaces

Each board state is evaluated using a **custom scoring function**, for example:

```
Score = α · EmptyCells
      + β · Monotonicity
      + γ · MaxTileInCorner
      + δ · MergePotential
```

The move with the highest expected score is selected.

These parameters are tuned experimentally to reduce the number of moves required to reach 2048.

---

## 📊 Performance Evaluation

The notebook measures:

* Total number of moves to reach 2048
* Win rate over multiple simulations
* Average max tile reached
* Stability of the board (entropy-like measures)

Multiple strategies can be compared by adjusting the heuristic weights.

## 🚀 How to Run

```bash
git clone https://github.com/<your-username>/2048-Solver.git
cd 2048-Solver
pip install -r requirements.txt

# Run the notebook
jupyter notebook notebooks/2048_solver.ipynb
```

Or run the manual version:

```bash
python src/game.py
```

---

## 🔮 Future Improvements

* Expectimax / Monte Carlo Tree Search (MCTS)
* Depth-limited lookahead
* Probabilistic modeling of tile spawns
* GPU-accelerated simulations
* Training a policy using reinforcement learning
