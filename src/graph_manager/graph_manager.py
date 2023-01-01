import networkx as nx


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def node(self, ref):
        print("warning")
        if ref not in self.graph.nodes:
            self.graph.add_node(ref)
        return self.graph.nodes[ref]

    def add_edge(self, node1: str, node2: str, weight: int):
        if node1 in self.graph and ndoe2 in self.graph[node1]:
            self.graph[node1][node2] += weight
        else:
            self.graph.add_edge(node1, node2, weight=weight)

    def size(self):
        return len(self.graph.nodes)

