#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Command Quest ===")
    program_name = sys.argv[0]
    print(f"Program name: {program_name}")

    total_args = len(sys.argv)

    user_args_count = total_args - 1

    if user_args_count == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {user_args_count}")
        index = 1
        for arg in sys.argv[1:]:
            print(f"Argument {index}: {arg}")
            index += 1

    print(f"Total arguments: {total_args}")


if __name__ == "__main__":
    main()
