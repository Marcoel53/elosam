from __future__ import annotations

from .models import BuildSpecification


class ValidationError(ValueError):
    """
    Raised when a build specification is invalid.
    """


class Validator:
    """
    Validates build specifications before compilation.
    """

    def validate(
        self,
        specification: BuildSpecification,
    ) -> None:

        if not specification.kind.strip():
            raise ValidationError("kind is required")

        if not specification.name.strip():
            raise ValidationError("name is required")