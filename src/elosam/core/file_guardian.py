"""
ELOSam FILE GUARDIAN (FINAL FIX)
Elimina BOM PERMANENTEMENTE no projeto.
"""

from pathlib import Path


class FileGuardian:
    @staticmethod
    def write(path: str, content: str):
        # normaliza caminho
        p = Path(path)

        # garante string limpa
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="ignore")

        # remove BOM invisível
        content = content.lstrip("\ufeff")

        # garante UTF-8 puro SEM BOM
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="\n")
