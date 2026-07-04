"""
ELOSam FINAL STABLE CORE FIX
Elimina U+FEFF + estabiliza escrita + corrige impacto infinito
"""

from pathlib import Path
import ast
from collections import defaultdict


# =========================
# FILE SAFE LAYER (FIX BOM)
# =========================
class SafeFile:
    @staticmethod
    def read(path: str) -> str:
        data = Path(path).read_bytes()

        # remove BOM se existir
        if data.startswith(b"\xef\xbb\xbf"):
            data = data[3:]

        return data.decode("utf-8", errors="ignore")

    @staticmethod
    def write(path: str, content: str):
        path = Path(path)

        # remove BOM invisível
        content = content.lstrip("\ufeff")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))


# =========================
# GRAPH ENGINE (SIMPLE)
# =========================
class GraphEngine:
    def build(self, root="src"):
        graph = {}
        for p in Path(root).rglob("*.py"):
            try:
                text = SafeFile.read(str(p))
                tree = ast.parse(text)
                imports = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            imports.append(n.name)
                    if isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)

                graph[str(p)] = imports
            except:
                continue

        return graph


# =========================
# IMPACT ENGINE (REAL)
# =========================
class ImpactEngine:
    def __init__(self):
        self.graph_engine = GraphEngine()
        self.last = None

    def analyze(self):
        graph = self.graph_engine.build()

        if self.last is None:
            self.last = graph
            return {
                "impact": 0.01,
                "status": "baseline"
            }

        old_keys = set(self.last.keys())
        new_keys = set(graph.keys())

        added = len(new_keys - old_keys)
        removed = len(old_keys - new_keys)

        score = (added + removed) / max(len(new_keys), 1)

        self.last = graph

        return {
            "impact": round(score, 3),
            "added": added,
            "removed": removed,
            "status": "active"
        }


# =========================
# RUNNER
# =========================
class Runner:
    def __init__(self):
        self.engine = ImpactEngine()

    def run(self):
        result = self.engine.analyze()
        print(result)


if __name__ == "__main__":
    Runner().run()
