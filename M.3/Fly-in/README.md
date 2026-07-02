*This project has been created as part of the 42 curriculum by oshtohri.*

# Fly-In

## Description
Fly-In is a Python 3.10+ project that simulates multiple drones moving through a network of connected zones. The goal is to route all drones from the start zone to the end zone while respecting movement costs, zone capacities, and connection capacities.

## Features
- Custom parser for Fly-in map files
- Graph-based pathfinding without external graph libraries
- Turn-based drone simulation
- Capacity-aware movement scheduling
- Terminal-based visualization with colored output
- Strict error handling and validation

- Terminal and Pygame visualizers: ANSI-colored headless output for CI and
	interactive Pygame UI for exploration and presentations.
- Deterministic, testable planner: BFS-seeded path candidates and
	heuristic scoring for reproducible routing decisions.
- Convenience targets: `Makefile` provides `install`, `run`, `run-visual`, `run-pygame`,
	`debug`, `lint`, and `clean` for quick workflows.
- Unit-tested core: `tests/` contains pytest cases covering parser,
	pathfinder, planner and simulator edge-cases.
- Self-contained graph & simulation code: no external graph libraries —
	easier debugging and portability between environments.
- Configurable playback: Pygame FPS and terminal modes are adjustable, and
	the visualizers support headless / "dummy" SDL runs for CI screenshots.
- Small-to-medium map focus: designed for clarity and correctness on the
	example maps provided (educational / subject-driven inputs).

## Project structure
```
.
├── README.md
├── Makefile
├── main.py
├── parser.py
├── pathfinder.py
├── planner.py
├── simulator.py
├── visualizer.py            # terminal visualizer (ANSI colors)
├── models.py
├── errors.py
├── pygame_visualizer/      # optional graphical UI (pygame)
│   ├── __init__.py
│   ├── board.py
│   ├── drones.py
│   ├── layout.py
│   ├── sidebar.py
│   ├── visualizer.py
│   └── zones.py
├── maps/                    # example map inputs used by the project
│   ├── easy/
│   ├── medium/
│   ├── hard/
│   └── challenger/
└── tests/
	├── test_parser.py
	├── test_pathfinder.py
	├── test_planner.py
	└── test_simulator.py
```

## Instructions
### Installation
```bash
make install
```

### Run
```bash
make run MAP=maps/easy/01_linear_path.txt
```

### Run visual on terminal
```bash
make run-visual MAP=maps/medium/02_circular_loop.txt
```

or directly:
```bash
python3 main.py maps/medium/02_circular_loop.txt --visual
```

### Run (pygame safe mode)
```bash
make run-pygame MAP=maps/medium/02_circular_loop.txt
```

or directly:
```bash
python3 main.py maps/medium/02_circular_loop.txt --pygame
```

### Debug
```bash
make debug MAP=maps/easy/01_linear_path.txt
```

### Lint
```bash
make lint
```

### Clean
```bash
make clean
```

## Algorithm
The implementation is split into three stages.

1. Parsing and graph construction
- The parser validates the full map syntax (unique hubs, valid connections, metadata, capacities, and zone types).
- Data is converted into an object-oriented graph (`Graph`, `Zone`, `Connection`, `Drone`).

2. Candidate path generation and scoring
- `PathFinder` uses BFS to find a base shortest path while ignoring blocked zones.
- `Planner` generates alternatives by temporarily banning selected edges or bottleneck nodes from the best path.
- Each candidate path is scored using a weighted heuristic:
	- movement cost by destination zone type (`normal=1`, `priority=1`, `restricted=2`),
	- penalties for restricted-heavy routes and bottlenecks,
	- bonus for priority zones,
	- estimated entry pressure and path capacity.
- Paths are sorted by this score and then assigned to drones using a Lem-in style turn-minimizing distribution (`T` search), with a greedy fallback.

3. Turn-based scheduling and conflict resolution
- The simulator executes one turn at a time and allows simultaneous drone actions.
- For each planned move, it enforces:
	- destination zone capacity (`max_drones`),
	- connection capacity (`max_link_capacity`),
	- blocked-zone prohibition.
- Restricted movement is modeled as a 2-turn transit:
	- turn N: output uses connection token (`D<ID>-<from-to>`),
	- turn N+1: forced arrival into the restricted zone (`D<ID>-<zone>`),
	- no waiting on connections is allowed.

Complexity notes:
- Parsing is linear in file size: `O(lines)`.
- BFS path search is `O(V + E)` per run.
- Candidate generation runs multiple BFS passes, so planning is roughly `O(k * (V + E))` for `k` variants.
- Simulation is proportional to simulated turns and drones, with constant-time capacity checks per attempted move.

### Why this approach?

- Simplicity & determinism: BFS-based shortest-path seeds (and multiple BFS passes for alternatives) produce deterministic, easy-to-reason-about candidates. This aligns with the 42 subject expectations and makes testing reproducible.
- Performance for typical inputs: maps in this project tend to be small-to-medium; BFS (O(V+E)) and repeated BFS for variants are fast and memory-light compared to heavier global optimizers.
- Capacity-aware planning: the Planner generates alternative routes by banning edges/nodes and scoring candidates using domain-specific heuristics (costs, priority zones, bottlenecks). This yields practical routes that respect zone/link capacities without requiring complex constraint solvers.
- Visual traceability: the generated plan is easy to explain and debug using the terminal and pygame visualizers — a design goal for both education and peer review.
- No external graph dependency: keeping the graph code in-project reduces hidden behavior, eases debugging, and keeps the solution portable.

## Visualization
The project provides two complementary visualizers: a colored terminal visualizer (enabled with `--visual`) and an optional Pygame UI (`--pygame`). Both read the same simulation snapshots so the core logic stays unchanged.

Terminal visualizer (`visualizer.py`):
- Usage: enabled by default when running normally; pass `--visual` or `make run-visual` to show detailed map and per-turn output.
- Output:
	- A colored list of zones and connections with human-readable metadata (start/goal, zone types, capacities).
	- Per-turn lines like `Turn N: D1-A D2-A-B` with drone IDs and destinations colorized.
	- A compact state summary showing each drone's status (idle, in-transit with remaining turns, or finished) and zone occupancy counts.
- Color & legend: uses ANSI escape codes to highlight starts (green), goals (red), priority zones (cyan), restricted zones (yellow), blocked zones (dim), and drones (bright magenta).
- Purpose: lightweight, fast, and ideal for automated runs, CI, and terminal-based debugging. No GUI dependencies required.

Pygame visualizer (`pygame_visualizer/`):
- Usage: run with `--pygame` or `make run-pygame` (requires `pygame` installed).
- Features:
	- Large board rendering of zones and connections with scalable layout.
	- Right-hand sidebar showing the current turn, drone counts, in-transit counts, recent moves, and controls.
	- Interactive controls: `SPACE` to pause/resume, `LEFT`/`RIGHT` to step backward/forward one frame, `Q` or `ESC` to quit.
	- Smooth playback with configurable FPS (default set in `PygameVisualizer(fps=...)`).
- Notes: the Pygame UI is a presentation layer only — it consumes the `TurnSnapshot` frames produced by the simulator and never modifies simulation logic. It supports a "challenge mode" layout for maps under `maps/challenger/` that uses different board sizing.

Both visualizers complement each other: the terminal view is scriptable and ideal for CI, while the Pygame view is interactive and excellent for exploratory debugging and presentations.

## Resources
- Python 3 docs: https://docs.python.org/3/
- dataclasses: https://docs.python.org/3/library/dataclasses.html
- collections.deque: https://docs.python.org/3/library/collections.html#collections.deque
- BFS overview: https://en.wikipedia.org/wiki/Breadth-first_search
- Dijkstra reference: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- Lem-in / multi-path distribution inspiration: (example subject and community resources)
- Pygame docs: https://www.pygame.org/docs/
- ANSI / terminal coloring reference: https://en.wikipedia.org/wiki/ANSI_escape_code

## AI Usage
AI was used to help structure the learning plan, explain graph and pathfinding concepts, and draft documentation. All implementation details were reviewed and understood manually before being kept.
