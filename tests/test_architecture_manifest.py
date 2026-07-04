from elosam.inspector.architecture_manifest import (
    ARCHITECTURE_LAYERS,
)


def test_manifest_contains_core_layers() -> None:
    names = [layer.name for layer in ARCHITECTURE_LAYERS]

    assert "application" in names
    assert "core" in names
    assert "capabilities" in names
    assert "inspector" in names