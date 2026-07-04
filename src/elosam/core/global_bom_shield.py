from pathlib import Path

class GlobalBOMShield:
    @staticmethod
    def clean_all(root="src"):
        for p in Path(root).rglob("*.py"):
            try:
                data = p.read_bytes()

                # remove BOM se existir
                if data.startswith(b"\xef\xbb\xbf"):
                    data = data[3:]

                text = data.decode("utf-8", errors="ignore").lstrip("\ufeff")

                p.write_bytes(text.encode("utf-8"))

            except Exception as e:
                print("SKIP:", p, e)

if __name__ == "__main__":
    GlobalBOMShield.clean_all()
    print("BOM SHIELD APPLIED")
