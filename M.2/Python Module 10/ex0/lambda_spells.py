#!/usr/bin/env python3
from typing import Any


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
        artifacts,
        key=lambda artifact: artifact["power"],
        reverse=True,
    )


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict[str, Any]:
    powers = list(map(lambda mage: mage["power"], mages))
    return {
        "max_power": max(powers),
        "min_power": min(powers),
        "avg_power": round(sum(powers) / len(powers), 2),
    }


def main() -> None:
    artifacts = [
        {'name': 'Water Chalice', 'power': 113, 'type': 'accessory'},
        {'name': 'Shadow Blade', 'power': 89, 'type': 'weapon'},
        {'name': 'Storm Crown', 'power': 65, 'type': 'relic'},
        {'name': 'Wind Cloak', 'power': 93, 'type': 'focus'},
    ]
    mages = [
        {'name': 'Luna', 'power': 58, 'element': 'ice'},
        {'name': 'Jordan', 'power': 85, 'element': 'wind'},
        {'name': 'Riley', 'power': 81, 'element': 'water'},
        {'name': 'Alex', 'power': 79, 'element': 'fire'},
        {'name': 'Ash', 'power': 88, 'element': 'shadow'}
    ]
    spells = ['shield', 'meteor', 'lightning', 'freeze']

    print("\nTesting artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    print(
        f"{sorted_artifacts[0]['name']} "
        f"({sorted_artifacts[0]['power']} power) "
        f"comes before {sorted_artifacts[1]['name']} "
        f"({sorted_artifacts[1]['power']} power)"
    )

    print("\nSorted artifacts:")
    for artifact in sorted_artifacts:
        print(f" - {artifact['name']} ({artifact['power']} power,"
              f" {artifact['type']})")

    print("\nTesting spell transformer...")
    print(" ".join(spell_transformer(spells)))

    print("\nTesting power filter...")
    strong_mages = power_filter(mages, 70)
    print("Mages with power >= 70:")
    for mage in strong_mages:
        print(f" - {mage['name']} ({mage['power']} power,"
              f" {mage['element']})")

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f" Max power: {stats['max_power']}")
    print(f" Min power: {stats['min_power']}")
    print(f" Avg power: {stats['avg_power']}")


if __name__ == "__main__":
    main()
