import pytest
from pathlib import Path

from parser import Parser
from errors import ParserError


def test_missing_nb_drones(tmp_path: Path) -> None:
    content = """# no nb_drones
start_hub: A 0 0
end_hub: B 1 0
"""
    p = tmp_path / "map.txt"
    p.write_text(content, encoding="utf-8")
    parser = Parser()
    with pytest.raises(ParserError):
        parser.parse(str(p))


def test_invalid_zone_metadata(tmp_path: Path) -> None:
    content = """nb_drones: 1
hub: A 0 0 [zone=unknown]
end_hub: B 1 0
"""
    p = tmp_path / "map.txt"
    p.write_text(content, encoding="utf-8")
    parser = Parser()
    with pytest.raises(ParserError):
        parser.parse(str(p))
