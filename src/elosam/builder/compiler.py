from __future__ import annotations

from pathlib import Path

from .build_report import BuildReport
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
    ) -> BuildReport:

        generated = self.generator.create_module(
            specification,
        )

        return BuildReport(
            specification=specification.name,
            generated=generated,
        )