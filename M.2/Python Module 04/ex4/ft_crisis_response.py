#!/usr/bin/env python3


def recover_archive_text(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file_handle:
        return file_handle.read()


def handle_access_attempt(filename: str, is_routine: bool) -> None:
    if is_routine:
        print(f"ROUTINE ACCESS: Attempting access to '{filename}'...")
    else:
        print(f"CRISIS ALERT: Attempting access to '{filename}'...")

    try:
        data = recover_archive_text(filename)
        print(f"SUCCESS: Archive recovered - ``{data}''")
        print("STATUS: Normal operations resumed")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained")
    except Exception:
        print("RESPONSE: Unexpected system anomaly encountered")
        print("STATUS: Crisis handled, system stable")

    print()


def main() -> None:
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===")
    print()

    handle_access_attempt("lost_archive.txt", is_routine=False)
    handle_access_attempt("classified_vault.txt", is_routine=False)
    handle_access_attempt("standard_archive.txt", is_routine=True)

    print("All crisis scenarios handled successfully. Archives secure.")


if __name__ == "__main__":
    main()
