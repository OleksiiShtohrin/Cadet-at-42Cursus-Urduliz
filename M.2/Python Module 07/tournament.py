#!/usr/bin/env python3
from ex0.factories import FlameFactory, AquaFactory
from ex1.factories import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    NormalStrategy,
    DefensiveStrategy,
    AggressiveStrategy,
    InvalidCreatureStrategyError,
)


def fight(opponent1, opponent2) -> None:
    factory1, strategy1 = opponent1
    factory2, strategy2 = opponent2

    creature1 = factory1.create_base()
    creature2 = factory2.create_base()

    print("* Battle *")
    print(creature1.describe())
    print(" vs.")
    print(creature2.describe())
    print(" now fight!")

    try:
        for line in strategy1.act(creature1):
            print(line)
        for line in strategy2.act(creature2):
            print(line)
    except InvalidCreatureStrategyError as exc:
        print(f"Battle error, aborting tournament: {exc}")


def tournament(opponents) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    print()

    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            fight(opponents[i], opponents[j])
            print()


def main() -> None:
    print("Tournament 0 (basic)")
    opponents0 = [
        (FlameFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    tournament(opponents0)

    print("Tournament 1 (error)")
    opponents1 = [
        (FlameFactory(), AggressiveStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    tournament(opponents1)

    print("Tournament 2 (multiple)")
    opponents2 = [
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ]
    print(" [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    tournament(opponents2)


if __name__ == "__main__":
    main()
