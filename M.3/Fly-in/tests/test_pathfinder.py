from pathfinder import PathFinder
from models import Graph, Zone, Connection


def _make_graph() -> Graph:
    g = Graph()
    g.add_zone(Zone("A", 0, 0))
    g.add_zone(Zone("B", 1, 0))
    g.add_zone(Zone("C", 0, 1))
    g.add_connection(Connection("A", "B"))
    g.add_connection(Connection("A", "C"))
    g.add_connection(Connection("C", "B"))
    return g


def test_shortest_path() -> None:
    pf = PathFinder()
    g = _make_graph()
    path = pf.find_shortest_path(g, "A", "B")
    assert path[0] == "A" and path[-1] == "B"


def test_alternative_path() -> None:
    pf = PathFinder()
    g = _make_graph()
    banned = {("A", "B")}
    alt = pf.find_alternative_path(g, "A", "B", banned_edges=banned)
    assert alt[0] == "A" and alt[-1] == "B"
    assert alt != ["A", "B"]
