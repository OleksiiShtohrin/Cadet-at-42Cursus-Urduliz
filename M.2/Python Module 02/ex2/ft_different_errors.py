#!/usr/bin/env python3

def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        _ = 1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        _ = "plant" + 1
    else:
        return


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")

    operations = [0, 1, 2, 3, 4]

    for op in operations:
        print(f"Testing operation {op}...")
        try:
            garden_operations(op)
            print("Operation completed successfully")
        except ValueError as exc:
            print(f"Caught ValueError: {exc}")
        except ZeroDivisionError as exc:
            print(f"Caught ZeroDivisionError: {exc}")
        except FileNotFoundError as exc:
            print(f"Caught FileNotFoundError: {exc}")
        except TypeError as exc:
            print(f"Caught TypeError: {exc}")

    print()
    print("Testing combined catch")
    try:
        garden_operations(0)
        garden_operations(1)
        print("Combined operations completed successfully")
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Caught ValueError or ZeroDivisionError: {exc}")

    print()
    print("All error types tested successfully!")


def main() -> None:
    test_error_types()


if __name__ == "__main__":
    main()
