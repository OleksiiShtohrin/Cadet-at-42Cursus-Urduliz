import pytest

from pathfinder import PathFinder
from models import Graph, Zone
from errors import PathFinderError


def test_no_path_raises() -> None:
    g = Graph()
    g.add_zone(Zone("A", 0, 0))
    g.add_zone(Zone("B", 1, 0))
    # no connection
    pf = PathFinder()
    with pytest.raises(PathFinderError):
        pf.find_shortest_path(g, "A", "B")
