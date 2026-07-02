#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)

    if temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    return temp


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===")
    print()

    tests: list[str] = ["25", "abc", "100", "-50"]

    for temp_str in tests:
        print(f"Input data is '{temp_str}'")
        try:
            temp = input_temperature(temp_str)
            print(f"Temperature is now {temp}°C")
            print()
        except Exception as exc:
            print(f"Caught input_temperature error: {exc}")
            print()

    print("All tests completed - program didn't crash!")


def main() -> None:
    test_temperature()


if __name__ == "__main__":
    main()
