from pathlib import Path

from elosam.knowledge.loader import KnowledgeLoader


def test_loader_reads_file(tmp_path: Path) -> None:
    document = tmp_path / "knowledge.txt"

    document.write_text(
        "Hello EloSam",
        encoding="utf-8",
    )

    loader = KnowledgeLoader()

    content = loader.load(document)

    assert content == "Hello EloSam"