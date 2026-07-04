class SafeWriter:
    @staticmethod
    def write(path, content):
        import os

        # for?a UTF-8 puro
        if content.startswith("\ufeff"):
            content = content.encode("utf-8-sig").decode("utf-8")

        with open(path, "wb") as f:
            f.write(content.encode("utf-8"))
