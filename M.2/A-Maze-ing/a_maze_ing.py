"""Main entry point for the A-Maze-ing v2.1 application.

This script loads the configuration file, creates a maze generator, writes
the output file, and provides an interactive terminal menu for regenerating
and redrawing the maze with different display options.

Usage:
    python3 a_maze_ing.py config.txt
    make run
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from mazegen.config import Config, load_config
from mazegen.generator import MazeGenerator
from mazegen.renderer import render_maze
from mazegen.writer import write_output


def clear_terminal() -> None:
    """Clear the terminal screen.

    This helper is used before redrawing the maze or the menu so the
    terminal output stays readable.
    """
    os.system("cls" if os.name == "nt" else "clear")


def _new_palette() -> dict[str, str]:
    """Create a random ANSI color palette for normal maze walls and path.

    The returned palette is used by the renderer to color the maze walls and
    the shortest path with random terminal colors.

    Returns:
        A dictionary containing ANSI escape codes for normal maze elements.
    """
    codes = random.sample(range(16, 231), 2)
    return {
        "wall": f"\x1b[38;5;{codes[0]}m",
        "path": f"\x1b[38;5;{codes[1]}m",
    }


def _new_palette_42() -> dict[str, str]:
    """Create a random ANSI color palette for the 42 pattern cells.

    This helper generates a random ANSI color used to highlight the visible
    42 pattern in the terminal renderer.

    Returns:
        A dictionary containing the ANSI escape code for the 42 pattern.
    """
    code = random.randint(16, 230)
    return {"cell42": f"\x1b[38;5;{code}m"}


@dataclass
class MazeState:
    """Store the current maze generation and display state.

    This object keeps the runtime configuration, the current generator
    instance, the used seed, and the display settings used by the menu.
    """

    width: int
    height: int
    entry: Tuple[int, int]
    exit_pos: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int]
    display_color: bool
    color_42: bool
    show_path: bool
    algorithm: str
    animate: bool
    animation_delay: float
    wall_palette: dict[str, str]
    palette_42: dict[str, str]
    used_seed: Optional[int] = None
    mg: Optional[MazeGenerator] = None


def _animate_frame(
    grid: list[list[int]],
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_pos: Tuple[int, int],
    state: MazeState,
) -> None:
    """Render and display one animation frame during maze generation.

    This function is used as part of the optional generation animation. It
    renders the current maze state, clears the terminal, prints the frame,
    and pauses briefly before the next update.

    Args:
        grid: Current maze grid being generated.
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry cell coordinates.
        exit_pos: Exit cell coordinates.
        state: Current runtime state with display settings.

    Returns:
        None.
    """
    rendered = render_maze(
        grid,
        width,
        height,
        entry,
        exit_pos,
        path=None,
        cells_42=set(),
        show_path=False,
        color=state.display_color,
        color_42=state.color_42,
        wall_palette=state.wall_palette,
        palette_42=state.palette_42,
    )
    clear_terminal()
    print(rendered)
    print(f"Algorithm: {state.algorithm}")
    time.sleep(state.animation_delay)


def _make_animation_callback(
    state: MazeState,
) -> Callable[[list[list[int]]], None]:
    """Create a callback used to display maze generation animation.

    The returned callback can be passed to MazeGenerator so that each
    generation step is rendered automatically during animation mode.

    Args:
        state: Current runtime state of the application.

    Returns:
        A callback function that accepts the current maze grid.
    """

    def _callback(grid: list[list[int]]) -> None:
        _animate_frame(
            grid,
            state.width,
            state.height,
            state.entry,
            state.exit_pos,
            state,
        )

    return _callback


def _toggle_algorithm_name(current: str) -> str:
    """Return the opposite maze generation algorithm name.

    This helper is used by the interactive menu to switch between DFS and
    Prim generation modes.

    Args:
        current: The current algorithm name.

    Returns:
        "PRIM" if the current algorithm is DFS, otherwise "DFS".
    """
    return "PRIM" if current.upper() == "DFS" else "DFS"


def _build_state(config: Config) -> MazeState:
    """Build the runtime state from a validated configuration.

    This function converts the parsed configuration object into a runtime
    state used by the interactive menu, renderer, animation, and generator.

    Args:
        config: Validated configuration loaded from the config file.

    Returns:
        A MazeState object containing both config data and UI settings.
    """
    return MazeState(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_pos=config.exit_pos,
        output_file=config.output_file,
        perfect=config.perfect,
        seed=config.seed,
        display_color=config.display_color,
        color_42=True,
        show_path=True,
        wall_palette=_new_palette(),
        palette_42=_new_palette_42(),
        algorithm=config.algorithm,
        animate=config.animate,
        animation_delay=config.animation_delay,
    )


def _generate_maze(state: MazeState) -> int:
    """Generate a maze and store the result in the current state.

    The function creates a MazeGenerator instance using the settings stored
    in the runtime state, runs generation, and saves the generated object
    back into state.mg.

    Any generation error is printed to stderr and reported as a non-zero
    return code.

    Args:
        state: Current runtime state of the application.

    Returns:
        0 on success, 1 if maze generation fails.
    """
    try:
        mg = MazeGenerator(
            width=state.width,
            height=state.height,
            seed=state.seed,
            entry=state.entry,
            exit_pos=state.exit_pos,
            perfect=state.perfect,
            include_42=True,
            algorithm=state.algorithm,
            on_step=_make_animation_callback(state) if state.animate else None,
        )
        mg.generate()
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if mg.path is None:
        print(
            "Error: Could not find a path from entry to exit.",
            file=sys.stderr
        )
        return 1

    state.mg = mg
    state.used_seed = mg.used_seed
    return 0


def _render_and_print(state: MazeState) -> int:
    """Write the maze output file and print the rendered maze to the terminal.

    This function expects a successfully generated maze. It writes the output
    file in the required format, clears the terminal, renders the maze, and
    prints additional information such as the seed, algorithm, and path
    length.

    Args:
        state: Current runtime state of the application.

    Returns:
        0 on success, 1 if the maze is not available.
    """
    if state.mg is None or state.mg.path is None:
        print("Error: Maze is not generated.", file=sys.stderr)
        return 1

    write_output(
        state.output_file,
        state.mg.grid,
        state.entry,
        state.exit_pos,
        state.mg.path,
    )

    clear_terminal()
    rendered = render_maze(
        state.mg.grid,
        state.width,
        state.height,
        state.entry,
        state.exit_pos,
        path=state.mg.path,
        cells_42=state.mg.cells_42,
        show_path=state.show_path,
        color=state.display_color,
        color_42=state.color_42,
        wall_palette=state.wall_palette,
        palette_42=state.palette_42,
    )

    if state.mg.skipped_42:
        print(
            "Warning: maze is too small for the 42 pattern; skipping it.\n"
            "Maze dimensions must be at least 9x7.\n"
        )

    print(rendered)
    print()

    if state.used_seed is not None:
        print(f"SEED : {state.used_seed}")
    print(f"Algorithm: {state.algorithm}")
    print(f"Maze written to '{state.output_file}'")
    print(f"Entry : {state.entry[0]},{state.entry[1]}")
    print(f"Exit  : {state.exit_pos[0]},{state.exit_pos[1]}")
    print(f"Path  : {len(state.mg.path)} steps")

    return 0


def _redraw_current(state: MazeState) -> int:
    """Redraw the current maze without regenerating it.

    This helper is used when the user changes display settings such as
    visible path, wall colors, 42 colors, or animation options. It only
    re-renders the current maze using the updated display state.

    Args:
        state: Current runtime state of the application.

    Returns:
        0 on success, 1 if no maze is currently available.
    """
    if state.mg is None:
        print("Error: No maze to redraw.", file=sys.stderr)
        return 1

    clear_terminal()
    rendered = render_maze(
        state.mg.grid,
        state.width,
        state.height,
        state.entry,
        state.exit_pos,
        path=state.mg.path,
        cells_42=state.mg.cells_42,
        show_path=state.show_path,
        color=state.display_color,
        color_42=state.color_42,
        wall_palette=state.wall_palette,
        palette_42=state.palette_42,
    )
    print(rendered)
    print()

    if state.used_seed is not None:
        print(f"SEED : {state.used_seed}")
    print(f"Algorithm: {state.algorithm}")
    print(f"Animation: {'ON' if state.animate else 'OFF'}")
    print(f"Maze written to '{state.output_file}'")
    print(f"Entry : {state.entry[0]},{state.entry[1]}")
    print(f"Exit  : {state.exit_pos[0]},{state.exit_pos[1]}")
    if state.mg.path is not None:
        print(f"Path  : {len(state.mg.path)} steps")
    return 0


def _generate_and_show(state: MazeState) -> int:
    """Generate a new maze and display it in the terminal.

    This helper combines generation and rendering into one action for the
    interactive menu. It first generates a maze and, if successful, writes
    the output file and prints the rendered maze.

    Args:
        state: Current runtime state of the application.

    Returns:
        0 on success, or a non-zero exit code if generation or rendering
        fails.
    """
    code = _generate_maze(state)
    if code != 0:
        return code

    return _render_and_print(state)


def run_menu(state: MazeState) -> int:
    """Run the interactive terminal menu for maze control.

    The menu allows the user to regenerate the maze, toggle the shortest
    path, change wall colors, change 42 colors, switch the generation
    algorithm, toggle animation, or quit the program.

    Args:
        state: Current runtime state of the application.

    Returns:
        0 on normal exit, or a non-zero exit code if one of the operations
        fails.
    """
    code = _generate_and_show(state)
    if code != 0:
        return code

    while True:
        print()
        print("--- A-Maze-ing menu ---")
        print("1. Regenerate maze")
        print("2. Show/Hide shortest path")
        print("3. Toggle wall color")
        print("4. Toggle 42 color")
        print("5. Toggle algorithm (DFS/PRIM)")
        print("6. Toggle animation")
        print("7. Quit")
        choice = input("Make your choice: ").strip()

        if choice == "1":
            code = _generate_and_show(state)
        elif choice == "2":
            state.show_path = not state.show_path
            code = _redraw_current(state)
        elif choice == "3":
            state.display_color = not state.display_color
            state.wall_palette = _new_palette()
            code = _redraw_current(state)
        elif choice == "4":
            state.color_42 = not state.color_42
            state.palette_42 = _new_palette_42()
            code = _redraw_current(state)
        elif choice == "5":
            state.algorithm = _toggle_algorithm_name(state.algorithm)
            code = _generate_and_show(state)
        elif choice == "6":
            state.animate = not state.animate
            print(f"Animation is now {'ON' if state.animate else 'OFF'}.")
            code = 0
        elif choice == "7":
            print("Bye.")
            return 0
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6 or 7.")
            code = 0

        if code != 0:
            return code


def main() -> int:
    """Program entry point.

    This function parses the command-line arguments, loads and validates the
    configuration file, builds the runtime state, and starts the interactive
    menu.

    Returns:
        0 on success, 1 if the configuration is invalid or another error
        occurs while starting the program.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="Path to the configuration file")
    args = parser.parse_args()

    try:
        config = load_config(args.config_file)
    except (ValueError, OSError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    state = _build_state(config)

    return run_menu(state)


if __name__ == "__main__":
    sys.exit(main())
