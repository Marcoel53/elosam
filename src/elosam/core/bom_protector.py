import pathlib

class BOMProtector:
    @staticmethod
    def clean_file(path):
        data = pathlib.Path(path).read_bytes()

        # remove BOM UTF-8 se existir
        if data.startswith(b"\xef\xbb\xbf"):
            data = data[3:]

        text = data.decode("utf-8", errors="ignore").lstrip("\ufeff")

        pathlib.Path(path).write_text(text, encoding="utf-8", newline="\n")
