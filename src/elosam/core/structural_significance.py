"""
STRUCTURAL SIGNIFICANCE ENGINE
Calcula importância real baseada em centralidade do sistema
"""

class StructuralSignificance:
    def __init__(self, graph: dict):
        self.graph = graph

    def compute_centrality(self):
        scores = {}

        for node, deps in self.graph.items():
            # importância = quantos dependem dele + quantos ele depende
            incoming = 0
            outgoing = len(deps)

            for _, d in self.graph.items():
                if node in d:
                    incoming += 1

            scores[node] = incoming + outgoing

        return scores

    def importance(self, affected: set):
        centrality = self.compute_centrality()

        total = sum(centrality.values()) or 1
        affected_score = sum(centrality.get(n, 0) for n in affected)

        return affected_score / total
