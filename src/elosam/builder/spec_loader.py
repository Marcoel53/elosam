from __future__ import annotations

import json
from pathlib import Path

from .models import BuildSpecification
from .validator import Validator


class SpecLoader:
    """
    Loads and validates build specifications.
    """

    def __init__(self) -> None:
        self.validator = Validator()

    def load(
        self,
        path: str | Path,
    ) -> BuildSpecification:

        data = json.loads(
            Path(path).read_text(
                encoding="utf-8",
            )
        )

        specification = BuildSpecification(
            kind=data["kind"],
            name=data["name"],
            models=data.get("models", False),
            contracts=data.get("contracts", False),
            exceptions=data.get("exceptions", False),
            tests=data.get("tests", False),
            readme=data.get("readme", False),
        )

        self.validator.validate(specification)

        return specification