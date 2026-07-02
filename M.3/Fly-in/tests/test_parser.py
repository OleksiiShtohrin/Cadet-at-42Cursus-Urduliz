from pathlib import Path

from parser import Parser


def test_parse_simple_map(tmp_path: Path) -> None:
    content = """nb_drones: 2
start_hub: A 0 0 [color=red max_drones=2]
end_hub: B 1 0
hub: C 0 1
connection: A-B
connection: A-C
connection: C-B
"""
    p = tmp_path / "map.txt"
    p.write_text(content, encoding="utf-8")

    parser = Parser()
    nb, graph = parser.parse(str(p))

    assert nb == 2
    assert set(graph.zones.keys()) == {"A", "B", "C"}
    assert graph.zones["A"].color == "red"
