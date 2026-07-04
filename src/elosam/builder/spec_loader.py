from __future__ import annotations

import json
from pathlib import Path

from .models import BuildSpecification


class SpecLoader:
    """
    Loads build specifications.
    """

    def load(
        self,
        path: str | Path,
    ) -> BuildSpecification:

        data = json.loads(
            Path(path).read_text(
                encoding="utf-8",
            )
        )

        return BuildSpecification(
            kind=data["kind"],
            name=data["name"],
            models=data.get("models", False),
            contracts=data.get("contracts", False),
            exceptions=data.get("exceptions", False),
            tests=data.get("tests", False),
            readme=data.get("readme", False),
        )