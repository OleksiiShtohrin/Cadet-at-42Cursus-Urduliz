#!/usr/bin/env python3

import random
from typing import Generator


def gen_event() -> Generator[tuple[str, str], None, None]:
    players: tuple[str, ...] = ("alice", "bob", "charlie", "dylan")
    actions: tuple[str, ...] = (
        "run",
        "eat",
        "sleep",
        "grab",
        "move",
        "climb",
        "swim",
        "release",
        "use",
    )

    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(
    events: list[tuple[str, str]],
) -> Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        index = random.randint(0, len(events) - 1)
        event = events[index]
        del events[index]
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    generator: Generator[tuple[str, str], None, None] = gen_event()

    i = 0
    while i < 1000:
        name, action = next(generator)
        print(f"Event {i}: Player {name} did action {action}")
        i += 1

    events: list[tuple[str, str]] = []
    i = 0
    while i < 10:
        events = events + [next(generator)]
        i += 1

    print(f"Built list of 10 events: {events}")

    for event in consume_event(events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    main()
