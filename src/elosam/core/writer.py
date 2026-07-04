from pathlib import Path

def write_py(path, content):
    p = Path(path)

    # remove BOM invisível
    content = content.lstrip("\ufeff")

    # normaliza newline
    content = content.replace("\r\n", "\n")

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")

    print(f"[OK] written: {path}")
