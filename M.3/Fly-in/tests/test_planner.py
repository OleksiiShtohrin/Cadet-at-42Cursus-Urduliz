from planner import Planner
from models import Graph, Zone, Connection


def test_build_and_assign() -> None:
    g = Graph()
    g.add_zone(Zone("A", 0, 0, is_start=True))
    g.add_zone(Zone("B", 1, 0, is_end=True))
    g.add_connection(Connection("A", "B"))

    planner = Planner(g)
    paths = planner.build_paths("A", "B")
    assert paths

    assignments = planner.assign_paths(3, paths)
    assert len(assignments) == 3
