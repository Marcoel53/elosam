from pathlib import Path

from elosam.builder.build_report import BuildReport


def test_build_report_counts_generated_files() -> None:
    report = BuildReport(
        specification="vision",
        generated=[
            Path("a.py"),
            Path("b.py"),
            Path("c.py"),
        ],
    )

    assert report.total_files == 3