from elosam.knowledge.knowledge_manifest import KNOWLEDGE_SOURCES


def test_knowledge_sources_exist() -> None:
    names = {source.name for source in KNOWLEDGE_SOURCES}

    assert "constitution" in names
    assert "adr" in names
    assert "rfc" in names
    assert "code" in names
    assert "tests" in names