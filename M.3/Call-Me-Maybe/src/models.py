"""Data models module.

Defines the structure and schema of input and output data using Pydantic.
Supports strict empty string and null-value validation.
"""

from typing import Any
from pydantic import BaseModel, Field, field_validator


class Prompt(BaseModel):
    """Pydantic model representing a prompt object."""

    prompt: str = Field(..., min_length=1)


class TypeDefinition(BaseModel):
    """Pydantic model representing parameter types."""

    type: str = Field(..., min_length=1)


class FunctionDefinition(BaseModel):
    """Pydantic model representing available function schema."""

    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    parameters: dict[str, TypeDefinition]
    returns: TypeDefinition

    @field_validator("parameters")
    @classmethod
    def validate_parameter_names(
        cls, v: dict[str, TypeDefinition]
    ) -> dict[str, TypeDefinition]:
        """Ensure parameter names (keys) are not empty or whitespace-only.

        Implements the 'Fail-Fast' principle, aborting execution during
        startup if the configuration file contains structural errors.
        """
        for key in v.keys():
            if not key.strip():
                raise ValueError(
                    "Parameter name (key) cannot be empty or whitespace-only."
                )
        return v


class FunctionCallResult(BaseModel):
    """Pydantic model validating final outputs for file saving."""

    prompt: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    parameters: dict[str, Any]

    @field_validator("parameters")
    @classmethod
    def validate_parameters(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Ensure no parameter value is null, whitespace-only,
        or an empty string.

        Args:
            v: The dictionary of extracted parameters.

        Returns:
            The validated parameters dictionary.

        Raises:
            ValueError: If a parameter is None or evaluated as an empty string.
        """
        for key, val in v.items():
            if val is None:
                raise ValueError(f"Parameter '{key}' cannot be null.")
            if isinstance(val, str):
                if not val.strip():
                    raise ValueError(
                        f"Parameter '{key}' cannot be an empty string."
                    )
        return v
