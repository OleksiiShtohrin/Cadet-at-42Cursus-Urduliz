#!/usr/bin/env python3


def build_archive_text() -> str:
    return (
        "[ENTRY 001] New quantum algorithm discovered\n"
        "[ENTRY 002] Efficiency increased by 347%\n"
        "[ENTRY 003] Archived by Data Archivist trainee\n"
    )


def write_new_archive(filename: str, content: str) -> None:
    file_handle = open(filename, "w", encoding="utf-8")
    try:
        file_handle.write(content)
    finally:
        file_handle.close()


def main() -> None:
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===")
    print()
    print("Initializing new storage unit: new_discovery.txt")
    print("Storage unit created successfully...")
    print()
    print("Inscribing preservation data...")

    print("[ENTRY 001] New quantum algorithm discovered")
    print("[ENTRY 002] Efficiency increased by 347%")
    print("[ENTRY 003] Archived by Data Archivist trainee")
    print()

    content = build_archive_text()
    write_new_archive("new_discovery.txt", content)

    print("Data inscription complete. Storage unit sealed.")
    print("Archive 'new_discovery.txt' ready for long-term preservation.")


if __name__ == "__main__":
    main()
