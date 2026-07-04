from __future__ import annotations

from pathlib import Path


class TemplateEngine:
    """
    Very small template renderer.
    """

    def render(
        self,
        template: Path,
        context: dict[str, str],
    ) -> str:

        text = template.read_text(
            encoding="utf-8",
        )

        for key, value in context.items():
            text = text.replace(
                "{{" + key + "}}",
                value,
            )

        return text