#!/usr/bin/env python3

import random


def main() -> None:
    print("=== Game Data Alchemist ===")
    print()

    players = [
        "Alice",
        "bob",
        "Charlie",
        "dylan",
        "Emma",
        "Gregory",
        "john",
        "kevin",
        "Liam",
    ]
    print(f"Initial list of players: {players}")

    capitalized_players = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {capitalized_players}")

    only_capitalized = [
        name for name in players if name[:1] == name[:1].upper()
    ]
    print(f"New list of capitalized names only: {only_capitalized}")
    print()

    score_min = 1
    score_max = 1000
    score_dict = {
        name: random.randint(score_min, score_max)
        for name in capitalized_players
    }
    print(f"Score dict: {score_dict}")

    total_score = sum(score_dict.values())
    avg = total_score / len(score_dict) if len(score_dict) > 0 else 0.0
    print(f"Score average is {round(avg, 2)}")

    high_scores = {
        name: score
        for name, score in score_dict.items()
        if score > avg
    }
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
