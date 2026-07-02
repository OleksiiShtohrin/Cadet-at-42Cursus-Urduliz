#!/usr/bin/env python3


def read_file_content(filename: str) -> str:
    file_handle = open(filename, "r", encoding="utf-8")
    try:
        content = file_handle.read()
        return content
    finally:
        file_handle.close()


def main() -> None:
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===")
    print()

    print("Accessing Storage Vault: ancient_fragment.txt")

    try:
        data = read_file_content("ancient_fragment.txt")
    except FileNotFoundError:
        print("ERROR:")
        print("Storage vault not found. Run data generator first.")
        return

    print("Connection established...")
    print()
    print("RECOVERED DATA:")
    print(data)
    print()
    print("Data recovery complete. Storage unit disconnected.")


if __name__ == "__main__":
    main()
