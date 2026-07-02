#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Abstract base class defining the common processing interface."""

    @abstractmethod
    def process(self, data: Any) -> str:
        """Process the data and return a result string."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate if data is appropriate for this processor."""
        raise NotImplementedError

    def format_output(self, result: str) -> str:
        """
        Default output formatting.

        In this subject we want to display:
        Output: <result>
        """
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    """Specialized processor for numeric lists."""

    def validate(self, data: Any) -> bool:
        if not isinstance(data, list):
            return False
        return all(isinstance(x, (int, float)) for x in data)

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                return self.format_output("Invalid numeric data")

            numbers = data
            count = len(numbers)
            total = sum(numbers)
            avg = total / count if count > 0 else 0.0

            return self.format_output(
                f"Processed {count} numeric values, sum={total}, avg={avg}"
            )
        except Exception as e:
            return self.format_output(f"Numeric processing error: {e}")


class TextProcessor(DataProcessor):
    """Specialized processor for strings."""

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                return self.format_output("Invalid text data")

            raw = data
            stripped = raw.strip()
            char_count = len(raw)
            word_count = len(
                [w for w in stripped.split(" ") if w != ""]
                ) if stripped else 0

            return self.format_output(
                f"Processed text: {char_count} characters, {word_count} words"
            )
        except Exception as e:
            return self.format_output(f"Text processing error: {e}")


class LogProcessor(DataProcessor):
    """Specialized processor for log entries (INFO/WARNING/ERROR)."""

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                return self.format_output("Invalid log entry")

            message = data.strip()

            level = "INFO"
            details = message

            if ":" in message:
                prefix, rest = message.split(":", 1)
                prefix = prefix.strip()
                if prefix != "":
                    level = prefix.upper()
                details = rest.strip()

            if level == "ERROR":
                prefix = "[ALERT]"
            elif level == "WARNING":
                prefix = "[WARN]"
            else:
                prefix = "[INFO]"

            return self.format_output(f"{prefix} {level} "
                                      f"level detected: {details}")
        except Exception as e:
            return self.format_output(f"Log processing error: {e}")


def demo_single_processor(
    processor: DataProcessor,
    processor_name: str,
    data: Any,
    data_repr: str,
    validation_msg: str,
) -> None:
    print(f"Initializing {processor_name}...")
    print(f"Processing data: {data_repr}")

    try:
        is_valid = processor.validate(data)
    except Exception:
        is_valid = False

    print("Validation:", validation_msg if is_valid else "Invalid data")
    print(processor.process(data))
    print()


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print()

    demo_single_processor(
        NumericProcessor(),
        "Numeric Processor",
        [1, 2, 3, 4, 5],
        "[1, 2, 3, 4, 5]",
        "Numeric data verified",
    )

    demo_single_processor(
        TextProcessor(),
        "Text Processor",
        "Hello Nexus World",
        '"Hello Nexus World"',
        "Text data verified",
    )

    demo_single_processor(
        LogProcessor(),
        "Log Processor",
        "ERROR: Connection timeout",
        '"ERROR: Connection timeout"',
        "Log entry verified",
    )

    print("=== Polymorphic Processing Demo ===")
    print()
    print("Processing multiple data types through same interface...")

    processors: list[DataProcessor] = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor(),
    ]
    samples: list[Any] = [
        [1, 2, 3],
        "Hello World!",
        "INFO: System ready",
    ]

    for idx, (proc, sample) in enumerate(zip(processors, samples), start=1):
        text = (f"Result {idx}: {proc.process(sample)}")
        new_text = text[:10] + text[18:]
        print(new_text)

    print()
    print("Foundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
