"""
SAFE FILE WRITER - ELOSAM CORE STANDARD
Elimina BOM (U+FEFF) e garante UTF-8 limpo.
"""

class SafeFileWriter:
    @staticmethod
    def write(path: str, content: str):
        # remove BOM se existir
        if content.startswith("\ufeff"):
            content = content.encode("utf-8").decode("utf-8-sig")

        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
