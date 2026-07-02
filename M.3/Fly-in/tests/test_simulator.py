from simulator import Simulator
from models import Graph, Zone, Connection


def test_simulator_run_one_drone() -> None:
    g = Graph()
    g.add_zone(Zone("A", 0, 0, is_start=True))
    g.add_zone(Zone("B", 1, 0, is_end=True))
    g.add_connection(Connection("A", "B"))

    sim = Simulator(g, 1)
    sim.initialize_drones("A", "B")
    sim.set_assignments({1: ["A", "B"]})
    snapshots = sim.run("A", "B")

    assert snapshots
    last = snapshots[-1]
    # final snapshot should show the drone finished
    assert last.drones[0].finished is True
