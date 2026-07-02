*This project has been created as part of the 42 curriculum by dzhambal and oshtohri*

# A-Maze-ing v2.1

## Description

A-Maze-ing is a Python project that generates a maze from a configuration file, solves it, writes the result to an output file, and displays the maze in the terminal. The project follows the requirements of the 42 curriculum and is designed to be reusable, testable, and easy to understand.

The program:
- reads a configuration file containing maze parameters,
- generates a random maze,
- finds the shortest path from entry to exit,
- writes the maze in the required hexadecimal format,
- prints an ASCII visualization of the maze,
- supports reproducible generation through a seed,
- provides a reusable maze generation module.

## Instructions

### Packaging Python Projects

```bash
# Installation from the wheel
pip install mazegen-1.0.0-py3-none-any.whl

# Installation from source code
pip install mazegen-1.0.0.tar.gz
```

### Requirements
- Python 3.10 or later

### Install dependencies
```bash
make install
```

### Run the program
```bash
python3 a_maze_ing.py config.txt
```
or
```
make run
```
This default command generates the maze, writes the output file, and prints one visual rendering.

## Interactive Menu

The terminal version includes an interactive menu that allows you to:

- regenerate the maze,
- show or hide the shortest path,
- change wall colors,
- change 42-pattern colors,
- switch between DFS and PRIM,
- animation toggle just changes setting,
- quit the program.

### Example configuration file
```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=False
SEED=42
DISPLAY_COLOR=True
ALGORITHM=DFS
ANIMATE=False
ANIMATION_DELAY=0.01
```

### Makefile commands
```bash
make install
make run
make debug
make clean
make test
make lint
make lint-strict
```

## Configuration File Format

The configuration file uses one `KEY=VALUE` pair per line.

Lines starting with `#` are comments and are ignored.

### Mandatory keys
- `WIDTH`: maze width in cells
- `HEIGHT`: maze height in cells
- `ENTRY`: entry coordinates in the form `x,y`
- `EXIT`: exit coordinates in the form `x,y`
- `OUTPUT_FILE`: output file name
- `PERFECT`: whether the maze must be perfect

### Optional keys
- `SEED`: integer seed for reproducible generation
- `DISPLAY_COLOR`: enables or disables colored rendering of the maze walls and path in the terminal
- `ALGORITHM`: chooses the maze generation algorithm (`DFS` or `PRIM`)
- `ANIMATE`: enables step-by-step maze generation animation in the terminal
- `ANIMATION_DELAY`: delay between animation frames in seconds

### Example
```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=1814624847
DISPLAY_COLOR=True
ALGORITHM=DFS
ANIMATE=True
ANIMATION_DELAY=0.01
```

## Maze Generation Algorithm

The project supports two maze generation algorithms:

- **DFS / recursive backtracker** — the default algorithm
- **Randomized Prim's algorithm** — available as a bonus option

### Why these algorithms were chosen
- DFS is simple, easy to explain, and produces perfect mazes naturally.
- Prim's algorithm produces a different maze style and demonstrates support for multiple algorithms, which is a bonus feature.

### How they work
- DFS goes deep into one branch until no unvisited neighbors remain, then backtracks.
- Prim's algorithm grows the maze from a frontier of walls and connects random neighboring cells.

### How to choose the algorithm
The algorithm can be selected in the configuration file:

```text
ALGORITHM=DFS
ALGORITHM=PRIM
```

## Why DFS algorithm was chosen

The maze is generated using a randomized depth-first search algorithm, also known as recursive backtracker.
- It is simple and easy to understand.
- It creates valid connected mazes.
- It works well for perfect mazes.
- It is suitable for reproducible random generation using a seed.

### How it works
- Start from one cell.
- Randomly choose an unvisited neighbor.
- Remove the wall between the current cell and the neighbor.
- Continue until every cell has been visited.
- Backtrack when a cell has no unvisited neighbors.

## Output File Format

The output file contains:
1. one hexadecimal digit per cell, row by row,
2. a blank line,
3. the entry coordinates,
4. the exit coordinates,
5. the shortest path from entry to exit using `N`, `E`, `S`, and `W`.

### Wall encoding
- `NORTH = 1`
- `EAST = 2`
- `SOUTH = 4`
- `WEST = 8`

A closed wall sets its bit to `1`, and an open wall sets it to `0`.

## Visual Representation

The project includes a terminal-based ASCII renderer.

The visual output shows:
- the maze walls,
- the entry cell,
- the exit cell,
- the solution path when available.

This satisfies the visual representation requirement and provides a simple way to inspect the maze without additional dependencies.
If the maze is too small to contain the visible 42 pattern, the program skips it and prints a warning to the console.

## Reusable Module

The `mazegen` package is provided as a reusable Python module and can be installed with `pip` from the included `.whl` or `.tar.gz` distribution files. After installation, it can be imported in another project.

It contains:
- `MazeGenerator` for maze creation,
- configuration parsing,
- path solving,
- file output serialization,
- terminal rendering.

### Basic example
```python
from mazegen import MazeGenerator

maze = MazeGenerator(width=20, height=15, seed=42, algorithm="DFS")
maze.generate()

grid = maze.grid
path = maze.path
cells_42 = maze.cells_42
```

### Reusability goal
The generator is separated into its own module so it can be imported into another Python project later.

## Project Structure

```text
Project-2-Python/
├── a_maze_ing.py
├── config.txt
├── Makefile
├── README.md
├── pyproject.toml
├── requirements.txt
├── tox.ini
├── .gitignore
└── mazegen/
    ├── __init__.py
    ├── config.py
    ├── generator.py
    ├── patterns.py
    ├── solver.py
    ├── writer.py
    └── renderer.py
└── tests/
    ├── __init__.py
    ├── test_config.py
    ├── test_generator.py
    ├── test_patterns.py
    ├── test_solver.py
    └── test_writer.py
```

## Tests

The project includes tests for:
- configuration parsing,
- maze generation,
- shortest path solving.

These tests are meant to help validate the logic during development.

```bash
python3 -m pytest
python3 -m pytest -q
```

## Bonus Features

This project is prepared for bonus features such as:
- support for multiple algorithms,
- animation during maze generation.

These bonuses improve usability and show how the project can be extended without breaking the core generation logic.

## Resources

### References
- Python documentation: https://docs.python.org/3/
- `dataclasses` documentation: https://docs.python.org/3/library/dataclasses.html
- `pathlib` documentation: https://docs.python.org/3/library/pathlib.html
- `collections.deque` documentation: https://docs.python.org/3/library/collections.html#collections.deque
- Maze generation algorithms overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Recursive backtracker explanation: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker

### AI usage
AI was used to:
- help structure the project into modules,
- explain maze generation and pathfinding concepts,
- draft documentation,
- clarify the expected output format,
- support learning and code understanding.

All generated ideas were reviewed, adapted, and understood before use.

## Team and Project Management

### Roles
This project was completed by:
- **dzhambal** — maze generation logic, reusable module structure, configuration parsing, and path solving.
- **oshtohri** — terminal rendering, menu interactions, output formatting, and documentation.

### Planning
The project was planned in stages:
1. understand the requirements,
2. design the module structure,
3. implement the generator,
4. add configuration parsing,
5. add shortest path solving,
6. implement output writing,
7. add visualization,
8. prepare documentation and tests,
9. integrate bonus features.

During development, the plan evolved as the implementation became clearer:
- first the core maze logic was implemented,
- then the reusable `mazegen` package was structured,
- after that the terminal menu and display logic were added,
- finally the README, Makefile, and tests were polished.

### What worked well
- splitting logic into small modules,
- using type hints,
- keeping the code readable,
- separating generation from rendering,
- validating configuration before maze generation.

### Tools used
- Python 3.10+
- Git / GitHub
- flake8
- mypy
- pytest
- AI tools for brainstorming, documentation drafting, and code review support

## License

This project is part of the 42 curriculum and is intended for educational use.
