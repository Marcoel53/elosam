from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BuildSpecification:
    """
    Immutable engineering specification.
    """

    kind: str
    name: str

    models: bool = False

    contracts: bool = False

    exceptions: bool = False

    tests: bool = False

    readme: bool = False