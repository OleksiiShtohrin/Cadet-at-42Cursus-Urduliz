import pytest

from planner import Planner
from models import Graph, Zone
from errors import PathFinderError


def test_planner_no_paths_raises() -> None:
    g = Graph()
    g.add_zone(Zone("A", 0, 0, is_start=True))
    g.add_zone(Zone("B", 1, 0, is_end=True))
    # no connection -> planner should raise when building paths
    planner = Planner(g)
    with pytest.raises(PathFinderError):
        planner.build_paths("A", "B")
