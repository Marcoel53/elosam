"""
AEGIS CORE Logging Manager.
"""

from __future__ import annotations

import logging
from pathlib import Path


class LoggingManager:
    """
    Centralized logging manager for the AEGIS runtime.
    """

    def __init__(self, name: str = "elosam") -> None:
        self._logger = logging.getLogger(name)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def configure(
        self,
        level: int = logging.INFO,
        log_file: str | None = None,
    ) -> None:
        self._logger.handlers.clear()
        self._logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self._logger.addHandler(console)

        if log_file is not None:
            path = Path(log_file)
            path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(
                path,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)
