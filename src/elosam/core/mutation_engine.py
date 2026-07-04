"""
ELOSam MUTATION ENGINE v1 (SAFE EVOLUTION CORE)
"""

from pathlib import Path
import random


class MutationEngine:
    def __init__(self, root="src"):
        self.root = Path(root)

    def pick_file(self):
        files = list(self.root.rglob("*.py"))
        return random.choice(files) if files else None

    def mutate(self, path: Path):
        text = path.read_text(encoding="utf-8", errors="ignore")

        # mutação segura: só adiciona comentário
        injection = f"\n# evolution_tick_{random.randint(1000,9999)}\n"

        new_text = text + injection
        path.write_text(new_text, encoding="utf-8")

        return str(path)


if __name__ == "__main__":
    engine = MutationEngine()
    file = engine.pick_file()

    if file:
        mutated = engine.mutate(file)
        print("MUTATED:", mutated)
    else:
        print("NO FILES FOUND")
