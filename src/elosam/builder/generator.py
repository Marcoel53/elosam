from __future__ import annotations

from pathlib import Path

from .writer import Writer


class ModuleGenerator:
    """
    Generates the basic package structure for a module.
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self.writer = Writer()

    def create_module(
        self,
        name: str,
    ) -> list[Path]:
        created: list[Path] = []

        package = self.root / name
        package.mkdir(
            parents=True,
            exist_ok=True,
        )

        files: dict[str, str] = {
            "__init__.py": "",
            f"{name}.py": f'''"""
{name.title()} Module
"""


class {name.title()}:
    pass
''',
            "contracts.py": '''"""
Contracts
"""
''',
            "models.py": '''"""
Models
"""
''',
            "exceptions.py": '''"""
Exceptions
"""
''',
            "README.md": f"# {name.title()}\n",
        }

        for filename, content in files.items():
            created.append(
                self.writer.write(
                    package / filename,
                    content,
                )
            )

        tests = Path("tests")

        tests.mkdir(
            exist_ok=True,
        )

        test_files = {
            f"test_{name}.py": f'''from elosam.{name}.{name} import {name.title()}


def test_import() -> None:
    assert {name.title()} is not None
''',
            f"test_{name}_models.py": '''def test_models_placeholder() -> None:
    assert True
''',
            f"test_{name}_contracts.py": '''def test_contracts_placeholder() -> None:
    assert True
''',
        }

        for filename, content in test_files.items():
            created.append(
                self.writer.write(
                    tests / filename,
                    content,
                )
            )

        return created