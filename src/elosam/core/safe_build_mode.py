from pathlib import Path

class SafeBuildMode:
    """
    Bloqueia criação insegura de arquivos Python
    e padroniza escrita UTF-8 SEM BOM.
    """

    @staticmethod
    def write_python(path: str, content: str):
        p = Path(path)

        # normalização total
        content = content.replace("\r\n", "\n")
        content = content.lstrip("\ufeff")

        # garante pasta
        p.parent.mkdir(parents=True, exist_ok=True)

        # escrita segura
        p.write_text(content, encoding="utf-8", newline="\n")

        print(f"[SAFE-BUILD] written: {p}")

    @staticmethod
    def validate(path: str):
        data = Path(path).read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            return False
        return True
