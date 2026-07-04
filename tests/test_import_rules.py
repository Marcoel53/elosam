from elosam.inspector.import_rules import FORBIDDEN_IMPORTS


def test_import_rules_exist() -> None:
    assert isinstance(FORBIDDEN_IMPORTS, dict)

    assert "elosam.application" in FORBIDDEN_IMPORTS