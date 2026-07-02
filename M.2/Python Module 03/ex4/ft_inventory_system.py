#!/usr/bin/env python3

import sys


def parse_argument(arg: str) -> tuple[bool, str, str]:
    colon_index = -1
    i = 0

    for char in arg:
        if char == ":":
            colon_index = i
            break
        i += 1

    if colon_index == -1:
        return (False, "", "")

    name = arg[:colon_index]
    quantity_str = arg[colon_index + 1:]

    if name == "" or quantity_str == "":
        return (False, "", "")

    return (True, name, quantity_str)


def parse_inventory(args: list[str]) -> tuple[dict[str, int], list[str]]:
    inventory: dict[str, int] = {}
    order: list[str] = []

    for arg in args:
        valid, name, quantity_str = parse_argument(arg)

        if not valid:
            print(f"Error - invalid parameter '{arg}'")
            continue

        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue

        try:
            quantity = int(quantity_str)
        except ValueError as exc:
            print(f"Quantity error for '{name}': {exc}")
            continue

        inventory[name] = quantity
        order = order + [name]

    return inventory, order


def main() -> None:
    print("=== Inventory System Analysis ===")

    args = sys.argv[1:]
    inventory, order = parse_inventory(args)

    print(f"Got inventory: {inventory}")

    item_list = list(inventory.keys())
    print(f"Item list: {item_list}")

    total_quantity = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total_quantity}")

    if total_quantity > 0:
        for item in order:
            percentage = round((inventory[item] / total_quantity) * 100, 1)
            print(f"Item {item} represents {percentage}%")
    else:
        for item in order:
            print(f"Item {item} represents 0.0%")

    if len(order) > 0:
        most_item = order[0]
        least_item = order[0]

        index = 1
        while index < len(order):
            item = order[index]
            if inventory[item] > inventory[most_item]:
                most_item = item
            if inventory[item] < inventory[least_item]:
                least_item = item
            index += 1

        print(
            f"Item most abundant: {most_item} "
            f"with quantity {inventory[most_item]}"
        )
        print(
            f"Item least abundant: {least_item} "
            f"with quantity {inventory[least_item]}"
        )

    inventory["magic_item"] = 1
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
