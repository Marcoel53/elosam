from pathlib import Path
import sys

TEMPLATE = '''"""
{name} Manager.
"""

from __future__ import annotations


class {name}Manager:
    """
    Auto-generated manager.
    """

    def __init__(self) -> None:
        pass
'''


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/create_manager.py <Name>")
        return 1

    name = sys.argv[1].strip()

    filename = f"{name.lower()}_manager.py"
    output = Path("src") / "elosam" / "core" / filename

    output.parent.mkdir(parents=True, exist_ok=True)

    if output.exists():
        print(f"{output} already exists.")
        return 1

    output.write_text(
        TEMPLATE.format(name=name),
        encoding="utf-8",
    )

    print(f"Created: {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
