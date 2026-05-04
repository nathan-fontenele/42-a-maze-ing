*This project has been created as part of the 42 curriculum by agomes-f, rafasilv*

## Description

A-Maze-ing is a terminal-based maze generator written in Python. It reads a configuration file, generates a maze (optionally perfect), displays it with ASCII art in the terminal, and saves the maze to a file using a hexadecimal wall representation. A solution path is computed and can be shown interactively.

## Instructions

### Requirements

- Python 3.10 or later
- `flake8` and `mypy` (for linting)

### Installation

```bash
make install
```

### Running

```bash
python3 a_maze_ing.py config.txt
```

Or with the Makefile:

```bash
make run
```

The program reads `config.txt` by default if no argument is given.

### Debug

```bash
make debug
```

### Lint

```bash
make lint
make lint-strict   # strict mypy mode
```

### Build the reusable package

```bash
make package
```

This produces `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` at the repository root.

### Install the reusable package

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Clean

```bash
make clean
```

## Configuration file format

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are comments.

| Key         | Description                           | Example              |
|-------------|---------------------------------------|----------------------|
| WIDTH       | Maze width in cells                   | `WIDTH=25`           |
| HEIGHT      | Maze height in cells                  | `HEIGHT=9`           |
| ENTRY       | Entry coordinates (x,y)               | `ENTRY=0,0`          |
| EXIT        | Exit coordinates (x,y)                | `EXIT=24,8`          |
| OUTPUT_FILE | Output filename for hex maze           | `OUTPUT_FILE=maze.txt` |
| PERFECT     | Whether the maze is perfect (True/False) | `PERFECT=True`    |
| SEED        | Optional seed for reproducibility     | `SEED=42`            |

Width must be between 9 and 45; height between 7 and 45. Entry and exit must be different and within bounds.

## Maze generation algorithm

Two algorithms are supported, selectable at runtime:

- **DFS (Depth-First Search / Recursive Backtracker)**: Carves passages by recursively visiting unvisited neighbors. Produces mazes with long, winding corridors and few dead ends.
- **BFS (Breadth-First Search)**: Carves passages level by level. Produces mazes with shorter, more uniform corridors.

When `PERFECT=False`, extra walls are randomly removed after generation to create loops.

## Why these algorithms

DFS was chosen as the primary algorithm because it naturally produces perfect mazes (spanning trees) with a simple recursive implementation. Its long corridors make the maze visually interesting. BFS was added as a bonus to give users a different feel, producing mazes with a more uniform structure.

## Reusable module

The `a_maze_ing` package (installable as `mazegen-*`) exposes a `MazeGenerator` class.

### Usage example

```python
from a_maze_ing import MazeGenerator

# Instantiate with a config file
gen = MazeGenerator("config.txt", animation=False)

# Generate using DFS
gen.dfs_generate()

# Solve the maze
gen.reset_maze_visited()
gen.start_solving()

# Access the maze grid
maze = gen.maze  # List[List[Cell]], each Cell has .walls (int, 0-15) and .static (bool)

# Get the shortest solution path
path = gen.shortest()  # e.g. "NEESSW..."

# Save hex output
gen.save_maze()

# Render to terminal
gen.render_frame()
```

### Custom parameters

```python
# Custom size and seed (via config file keys WIDTH, HEIGHT, SEED)
# Or access the maze directly after generation:
gen.WIDTH   # int
gen.HEIGHT  # int
gen.seed    # int
gen.ENTRY   # Dict[str, int] with keys 'x' and 'y'
gen.EXIT    # Dict[str, int] with keys 'x' and 'y'
```

### Accessing solutions

```python
gen.solutions        # List[List[str]] — all found paths
gen.shortest()       # str — directions as N/E/S/W letters (shortest path)
```

The `Cell` class has:
- `walls: int` — bitmask (bit 0 = North, 1 = East, 2 = South, 3 = West; 1 = wall closed)
- `static: bool` — True for cells that are part of the "42" pattern
- `visited: bool` — used during generation/solving

## Team and project management

**Team:** nathan-fontenele (solo project)

**Roles:** All development, testing, and documentation by nathan-fontenele.

**Planning:** Initial setup included the core generator and terminal UI. The DFS algorithm was implemented first, followed by the BFS variant, solver, and saving features. Bonus features (animation, multiple solution styles, wall customization) were added after the mandatory part was complete.

**What worked well:** The bitmask wall representation kept the maze data compact and made serialisation straightforward. Using a config file for parameters made the program flexible without recompilation.

**What could be improved:** The recursive DFS hits Python's recursion limit on very large mazes; an iterative version would be more robust. The multiple-paths approach for non-perfect mazes does not guarantee corridor width constraints on all seeds.

**Tools used:** Python 3, flake8, mypy, pdb for debugging. AI assistance (Claude) was used to review code structure and docstrings.

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker (DFS)](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Python typing module documentation](https://docs.python.org/3/library/typing.html)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)

**AI usage:** Claude was used to review docstring formatting, check PEP 257 compliance, and suggest improvements to exception handling. All algorithmic logic (DFS, BFS, solver, hex encoding) was written and understood by the author.
