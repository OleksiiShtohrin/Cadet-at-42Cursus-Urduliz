from __future__ import annotations

"""Command-line entry point for the Fly-in simulator.

This module parses CLI arguments, builds a plan using `Planner`, runs the
`Simulator`, and optionally renders output using either the simple ASCII
`Visualizer` or the `PygameVisualizer`.

Example:
    python main.py maps/easy/01_linear_path.txt
    python main.py maps/easy/01_linear_path.txt --visual
    python main.py maps/easy/01_linear_path.txt --pygame
"""

import sys
from pathlib import Path
from typing import Dict, List

from errors import FlyInError
from parser import Parser
from planner import Planner
from pygame_visualizer import PygameVisualizer
from simulator import Simulator
from visualizer import Visualizer


def main() -> int:
    """Run the Fly-in application.

    Returns:
        int: Exit code (0 on success, non-zero on error).
    """
    args = sys.argv[1:]

    if not args or len(args) > 2:
        print("Usage: python main.py <map_file> [--visual|--pygame]")
        return 1

    map_path = args[0]
    visual_mode = False
    pygame_mode = False

    if len(args) == 2:
        if args[1] == "--visual":
            visual_mode = True
        elif args[1] == "--pygame":
            pygame_mode = True
        else:
            print("Usage: python main.py <map_file> [--visual|--pygame]")
            return 1

    try:
        parser = Parser()
        nb_drones, graph = parser.parse(map_path)

        start_zone = next(
            zone.name for zone in graph.zones.values() if zone.is_start
        )
        goal_zone = next(
            zone.name for zone in graph.zones.values() if zone.is_end
        )

        planner = Planner(graph)
        paths = planner.build_paths(start_zone, goal_zone)
        assignments_list = planner.assign_paths(nb_drones, paths)

        assignments: Dict[int, List[str]] = {
            i + 1: assignments_list[i] for i in range(nb_drones)
        }

        visualizer = Visualizer(enabled=visual_mode, total_drones=nb_drones)
        if visual_mode and not pygame_mode:
            visualizer.render_map(graph)

        simulator = Simulator(graph, nb_drones)
        simulator.initialize_drones(start_zone, goal_zone)
        simulator.set_assignments(assignments)

        snapshots = simulator.run_with_snapshots(start_zone, goal_zone)

        if pygame_mode:
            pygame_visualizer = PygameVisualizer(fps=1.6)
            map_title = Path(map_path).stem.replace("_", " ")
            pygame_visualizer.run(
                graph,
                snapshots,
                map_title=map_title,
                map_path=map_path,
            )
        else:
            for snapshot in snapshots:
                if visual_mode:
                    visualizer.render_turn(
                        snapshot.turn_index,
                        snapshot.moves,
                        graph,
                    )
                    visualizer.render_state(
                        snapshot.drones,
                        graph,
                        snapshot.zone_occupancy,
                    )
                else:
                    for line in snapshot.moves:
                        print(line)

    except FlyInError as error:
        print(f"Error: {error}")
        return 1
    except RuntimeError as error:
        print(f"Error: {error}")
        return 1
    except StopIteration:
        print("Error: Map must contain exactly one start_hub and one end_hub")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
