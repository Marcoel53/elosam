from __future__ import annotations

from pathlib import Path

from .generator import ModuleGenerator
from .models import BuildSpecification


class Compiler:
    """
    Engineering compiler.
    """

    def __init__(self) -> None:
        self.generator = ModuleGenerator(
            Path("src/elosam"),
        )

    def compile(
        self,
        specification: BuildSpecification,
    ):
        return self.generator.create_module(
            specification.name,
        )