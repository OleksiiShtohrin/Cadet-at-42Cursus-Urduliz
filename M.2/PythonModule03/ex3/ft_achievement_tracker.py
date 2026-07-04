#!/usr/bin/env python3

import random


def gen_player_achievements() -> set[str]:
    all_achievements = (
        "Crafting Genius",
        "Strategist",
        "World Savior",
        "Speed Runner",
        "Survivor",
        "Master Explorer",
        "Treasure Hunter",
        "Unstoppable",
        "First Steps",
        "Collector Supreme",
        "Untouchable",
        "Sharp Mind",
        "Boss Slayer",
        "Hidden Path Finder",
        "Legendary Hero",
        "Puzzle Master",
    )

    count = random.randint(3, 7)
    player_achievements: set[str] = set()

    while len(player_achievements) < count:
        player_achievements.add(random.choice(all_achievements))

    return player_achievements


def main() -> None:
    print("=== Achievement Tracker System ===")
    print()

    player_names = ("Alice", "Bob", "Charlie", "Dylan")
    players: dict[str, set[str]] = {}

    index = 0
    while index < len(player_names):
        name = player_names[index]
        players[name] = gen_player_achievements()
        print(f"Player {name}: {players[name]}")
        index += 1

    print()

    all_distinct: set[str] = set()
    common: set[str] = players[player_names[0]]

    index = 0
    while index < len(player_names):
        name = player_names[index]
        all_distinct = all_distinct.union(players[name])
        common = common.intersection(players[name])
        index += 1

    print(f"All distinct achievements: {all_distinct}")
    print()
    print(f"Common achievements: {common}")
    print()

    index = 0
    while index < len(player_names):
        name = player_names[index]
        others: set[str] = set()

        other_index = 0
        while other_index < len(player_names):
            other_name = player_names[other_index]
            if other_name != name:
                others = others.union(players[other_name])
            other_index += 1

        only_this_player = players[name].difference(others)
        print(f"Only {name} has: {only_this_player}")
        index += 1

    print()

    index = 0
    while index < len(player_names):
        name = player_names[index]
        missing = all_distinct.difference(players[name])
        print(f"{name} is missing: {missing}")
        index += 1


if __name__ == "__main__":
    main()
