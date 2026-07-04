"""
GRAPH STATE MEMORY ENGINE
Stores previous graph snapshot for delta analysis
"""

import copy


class GraphStateMemory:
    def __init__(self):
        self.previous_graph = None

    def update(self, graph: dict):
        old = self.previous_graph
        self.previous_graph = copy.deepcopy(graph)
        return old, graph

    def has_previous(self):
        return self.previous_graph is not None
