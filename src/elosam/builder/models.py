from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BuildSpecification:
    """
    Immutable build specification.
    """

    kind: str

    name: str

    models: bool = False

    contracts: bool = False

    exceptions: bool = False

    tests: bool = False

    readme: bool = False


@dataclass(slots=True, frozen=True)
class BuildContext:
    """
    Rendering context used by templates.
    """

    module_name: str

    class_name: str

    @classmethod
    def from_specification(
        cls,
        specification: BuildSpecification,
    ) -> "BuildContext":
        return cls(
            module_name=specification.name,
            class_name=specification.name.title(),
        )