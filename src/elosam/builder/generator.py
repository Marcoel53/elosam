from __future__ import annotations

from pathlib import Path

from .models import BuildContext
from .models import BuildSpecification
from .renderer import Renderer
from .writer import Writer


class ModuleGenerator:
    """
    Generates capability packages from templates.
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self.writer = Writer()
        self.renderer = Renderer()

    def create_module(
        self,
        specification: BuildSpecification,
    ) -> list[Path]:

        created: list[Path] = []

        context = BuildContext.from_specification(
            specification,
        )

        package = self.root / context.module_name

        package.mkdir(
            parents=True,
            exist_ok=True,
        )

        template_root = Path(
            "src/elosam/builder/templates/capability"
        )

        templates = {
            "__init__.py": "",
            f"{context.module_name}.py": self.renderer.render(
                template_root / "module.tpl",
                context.__dict__,
            ),
            "models.py": self.renderer.render(
                template_root / "models.tpl",
                context.__dict__,
            ),
            "contracts.py": self.renderer.render(
                template_root / "contracts.tpl",
                context.__dict__,
            ),
            "exceptions.py": self.renderer.render(
                template_root / "exceptions.tpl",
                context.__dict__,
            ),
            "README.md": self.renderer.render(
                template_root / "readme.tpl",
                context.__dict__,
            ),
        }

        for filename, content in templates.items():
            created.append(
                self.writer.write(
                    package / filename,
                    content,
                )
            )

        created.append(
            self.writer.write(
                Path("tests") / f"test_{context.module_name}.py",
                self.renderer.render(
                    template_root / "test.tpl",
                    context.__dict__,
                ),
            )
        )

        return created