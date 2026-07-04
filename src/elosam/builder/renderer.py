from __future__ import annotations

from pathlib import Path

from .template_engine import TemplateEngine


class Renderer:
    """
    Renders templates using a context.
    """

    def __init__(self) -> None:
        self.engine = TemplateEngine()

    def render(
        self,
        template: Path,
        context: dict[str, str],
    ) -> str:
        return self.engine.render(
            template,
            context,
        )