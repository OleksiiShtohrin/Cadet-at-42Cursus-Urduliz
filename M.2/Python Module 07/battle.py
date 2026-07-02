#!/usr/bin/env python3
from ex0 import FlameFactory, AquaFactory


def test_factory(factory) -> None:
    print("Testing factory")
    try:
        base = factory.create_base()
        evolved = factory.create_evolved()

        print(base.describe())
        print(base.attack())
        print(evolved.describe())
        print(evolved.attack())
        print()
    except Exception as exc:
        print(f"Error during battle setup: {exc}")


def battle(factory1, factory2) -> None:
    print("Testing battle")
    try:
        creature1 = factory1.create_base()
        creature2 = factory2.create_base()

        print(creature1.describe())
        print(" vs.")
        print(creature2.describe())
        print(" fight!")
        print(creature1.attack())
        print(creature2.attack())
    except Exception as exc:
        print(f"Error during battle setup: {exc}")


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    test_factory(flame_factory)
    test_factory(aqua_factory)
    battle(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()
