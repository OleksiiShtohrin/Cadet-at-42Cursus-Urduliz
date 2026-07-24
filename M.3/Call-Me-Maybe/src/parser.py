"""Parser module.

Utility methods for parsing and validating function definitions and prompts.
"""

import json
from src.models import FunctionDefinition, Prompt


def parse_function_definitions(path: str) -> list[FunctionDefinition]:
    """Parse and validate functions definitions file.

    Args:
        path: File path to the JSON file containing function definitions.

    Returns:
        A list of validated FunctionDefinition models.
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        FunctionDefinition(**function)
        for function in data
    ]


def parse_test_prompts(path: str) -> list[Prompt]:
    """Parse and validate test prompts file.

    Args:
        path: File path to the JSON file containing prompts.

    Returns:
        A list of validated Prompt models.
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Prompt(**prompt) for prompt in data]
