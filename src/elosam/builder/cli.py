from __future__ import annotations

import argparse

from .compiler import Compiler
from .spec_loader import SpecLoader


class BuilderCLI:
    """
    AEGIS Builder Command Line Interface.
    """

    def __init__(self) -> None:
        self.loader = SpecLoader()
        self.compiler = Compiler()

    def run(self) -> None:
        parser = argparse.ArgumentParser(
            prog="elosam-builder",
            description="AEGIS Engineering Builder",
        )

        subparsers = parser.add_subparsers(
            dest="command",
            required=True,
        )

        build = subparsers.add_parser(
            "build",
            help="Build from specification",
        )

        build.add_argument(
            "spec",
            help="JSON specification file",
        )

        args = parser.parse_args()

        if args.command == "build":
            self.build(args.spec)

    def build(
        self,
        specification: str,
    ) -> None:
        spec = self.loader.load(specification)

        created = self.compiler.compile(spec)

        print()
        print("=" * 50)
        print("AEGIS ENGINEERING BUILDER")
        print("=" * 50)
        print(f"Kind : {spec.kind}")
        print(f"Name : {spec.name}")
        print()

        for file in created:
            print(f"[OK] {file}")

        print()
        print(f"Generated files : {len(created)}")
        print("=" * 50)


def main() -> None:
    BuilderCLI().run()


if __name__ == "__main__":
    main()