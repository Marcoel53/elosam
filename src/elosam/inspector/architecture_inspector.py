"""
Architecture Inspector

Constitutional validation utilities.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class InspectionResult:
    passed: bool
    rule: str
    message: str


class ArchitectureInspector:
    """
    First constitutional inspector.

    This MVP validates architectural rules.
    """

    def validate(
        self,
        condition: bool,
        rule: str,
    ) -> InspectionResult:

        if condition:
            return InspectionResult(
                passed=True,
                rule=rule,
                message="passed",
            )

        return InspectionResult(
            passed=False,
            rule=rule,
            message="failed",
        )