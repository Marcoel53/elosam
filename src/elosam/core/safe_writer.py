from pathlib import Path

class SafePythonWriter:
    @staticmethod
    def write(path: str, content: str):
        p = Path(path)

        # força UTF-8 limpo SEM BOM
        if content.startswith("\ufeff"):
            content = content.lstrip("\ufeff")

        # garante newline padrão
        p.write_text(content, encoding="utf-8", newline="\n")

    @staticmethod
    def write_file(path: str, content: str):
        SafePythonWriter.write(path, content)
