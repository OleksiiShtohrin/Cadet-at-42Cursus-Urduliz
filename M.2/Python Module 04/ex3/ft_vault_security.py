#!/usr/bin/env python3


def secure_read(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file_handle:
        return file_handle.read()


def secure_write(filename: str, content: str) -> None:
    with open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(content)


def main() -> None:
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===")
    print()
    print("Initiating secure vault access...")
    print("Vault connection established with failsafe protocols")
    print()
    print("SECURE EXTRACTION:")

    data = secure_read("classified_data.txt")
    print(data)
    print()
    print("SECURE PRESERVATION:")

    new_protocol = "[CLASSIFIED] New security protocols archived\n"
    secure_write("security_protocols.txt", new_protocol)

    print("[CLASSIFIED] New security protocols archived")
    print("Vault automatically sealed upon completion")
    print()
    print("All vault operations completed with maximum security.")


if __name__ == "__main__":
    main()
