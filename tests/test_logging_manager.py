import logging
from pathlib import Path

from elosam.core.logging_manager import LoggingManager


def test_logger_name() -> None:
    manager = LoggingManager("test")

    assert manager.logger.name == "test"


def test_configure() -> None:
    manager = LoggingManager("test")

    manager.configure()

    assert manager.logger.level == logging.INFO
    assert len(manager.logger.handlers) >= 1


def test_log_file(tmp_path: Path) -> None:
    logfile = tmp_path / "elosam.log"

    manager = LoggingManager("test")
    manager.configure(log_file=str(logfile))

    manager.info("Hello EloSam")

    assert logfile.exists()
