"""
AEGIS AUTONOMOUS SAFE APPLY ENGINE.
Applies real code mutations with rollback safety.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import shutil
import os


@dataclass
class ApplyResult:
    file: str
    status: str
    backup: str | None


class SafeApplyEngine:
    """
    Applies real patches safely with backup + rollback.
    """

    def apply(self, patch: Any) -> ApplyResult:
        real_patch = getattr(patch, "patch", None)

        if real_patch is None:
            return ApplyResult(
                file="unknown",
                status="no_patch_found",
                backup=None,
            )

        file_path = real_patch.file

        # create backup first (ROLLBACK SAFETY)
        backup_path = file_path + ".bak"

        try:
            if os.path.exists(file_path):
                shutil.copy(file_path, backup_path)

            # APPLY PATCH (controlled write)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(real_patch.after)

            return ApplyResult(
                file=file_path,
                status="applied",
                backup=backup_path,
            )

        except Exception as e:
            # rollback
            if os.path.exists(backup_path):
                shutil.copy(backup_path, file_path)

            return ApplyResult(
                file=file_path,
                status=f"failed_and_rolled_back: {str(e)}",
                backup=backup_path,
            )
