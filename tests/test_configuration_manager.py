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
import json
from pathlib import Path

from elosam.core.configuration_manager import ConfigurationManager


def test_default_value() -> None:
    config = ConfigurationManager()

    assert config.get("missing", "default") == "default"


def test_overwrite_value() -> None:
    config = ConfigurationManager()

    config.set("key", 1)
    config.set("key", 2)

    assert config.get("key") == 2


def test_multiple_values() -> None:
    config = ConfigurationManager()

    config.set("host", "localhost")
    config.set("port", 8080)

    assert config.get("host") == "localhost"
    assert config.get("port") == 8080


def test_data_returns_copy() -> None:
    config = ConfigurationManager()

    config.set("name", "elosam")

    data = config.data
    data["name"] = "changed"

    assert config.get("name") == "elosam"


def test_load_empty_file(tmp_path: Path) -> None:
    file = tmp_path / "config.json"

    file.write_text(
        json.dumps({}),
        encoding="utf-8",
    )

    config = ConfigurationManager()

    config.load(file)

    assert config.data == {}
