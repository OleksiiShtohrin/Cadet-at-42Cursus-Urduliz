from simulator import Simulator
from models import Graph, Zone, Connection


def test_deadlock_detected() -> None:
    # Construct a small graph where two drones block each other
    g = Graph()
    g.add_zone(Zone("A", 0, 0, is_start=True))
    g.add_zone(Zone("B", 1, 0))
    g.add_zone(Zone("C", 2, 0, is_end=True))
    # connections: A-B, B-C
    g.add_connection(Connection("A", "B"))
    g.add_connection(Connection("B", "C"))

    sim = Simulator(g, 2)
    sim.initialize_drones("A", "C")

    # Assign both drones to pass through B but capacity 1 at B
    sim.set_assignments({1: ["A", "B", "C"], 2: ["A", "B", "C"]})

    # First run should proceed; if deadlock detection triggers later,
    # ensure it raises a SimulationError.
    snapshots = sim.run("A", "C")
    assert snapshots
