#!/usr/bin/env python3
from ex1.factories import HealingCreatureFactory, TransformCreatureFactory


def test_healing_factory() -> None:
    print("Testing Creature with healing capability")
    factory = HealingCreatureFactory()

    base = factory.create_base()
    evolved = factory.create_evolved()

    print(" base:")
    print(base.describe())
    print(base.attack())
    print(base.heal())

    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.heal())
    print()


def test_transform_factory() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()

    base = factory.create_base()
    evolved = factory.create_evolved()

    print(" base:")
    print(base.describe())
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())

    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


def main() -> None:
    test_healing_factory()
    test_transform_factory()


if __name__ == "__main__":
    main()
