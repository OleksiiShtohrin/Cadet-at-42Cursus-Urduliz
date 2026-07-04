#!/usr/bin/env python3

import sys


def write_stdout(message: str) -> None:
    sys.stdout.write(message + "\n")


def write_stderr(message: str) -> None:
    sys.stderr.write(message + "\n")


def main() -> None:
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===")
    print()

    archivist_id = input("Input Stream active. Enter archivist ID: ")
    status_report = input("Input Stream active. Enter status report: ")
    print()

    write_stdout(f"[STANDARD] Archive status "
                 f"from {archivist_id}: {status_report}")
    write_stderr("[ALERT] System diagnostic: Communication channels verified")
    write_stdout("[STANDARD] Data transmission complete")
    print()
    print("Three-channel communication test successful.")


if __name__ == "__main__":
    main()
