"""
GRAPH SNAPSHOT ENGINE
Captura estado estrutural do sistema
"""

import copy


class GraphSnapshotEngine:
    def __init__(self):
        self.last_snapshot = None

    def snapshot(self, graph: dict):
        current = copy.deepcopy(graph)
        previous = self.last_snapshot
        self.last_snapshot = current
        return previous, current
