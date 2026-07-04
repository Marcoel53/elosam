from pathlib import Path

class AtomicWriter:
    @staticmethod
    def write(path, content):
        p = Path(path)

        # garante limpeza absoluta
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="ignore")

        content = content.lstrip("\ufeff")

        p.write_text(content, encoding="utf-8", newline="\n")
