import json
from pathlib import Path

from elosam.core.configuration_manager import ConfigurationManager


def test_set_get() -> None:
    config = ConfigurationManager()

    config.set("host", "localhost")

    assert config.get("host") == "localhost"


def test_has() -> None:
    config = ConfigurationManager()

    config.set("port", 8080)

    assert config.has("port")
    assert not config.has("debug")


def test_clear() -> None:
    config = ConfigurationManager()

    config.set("name", "elosam")
    config.clear()

    assert config.data == {}


def test_load(tmp_path: Path) -> None:
    file = tmp_path / "config.json"

    file.write_text(
        json.dumps(
            {
                "name": "elosam",
                "version": "0.1.0",
            }
        ),
        encoding="utf-8",
    )

    config = ConfigurationManager()

    config.load(file)

    assert config.get("name") == "elosam"
    assert config.get("version") == "0.1.0"
