import networkx as nx


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def node(self, ref):
        print("warning")
        if ref not in self.graph.nodes:
            self.graph.add_node(ref)
        return self.graph.nodes[ref]

    def add_node_type(self, node, node_type):
        self.graph.add_node(node, type=node_type)

    def add_edge(self, node1: str, node2: str, **attrs):
        if self.graph.has_edge(node1, node2):
            for attr, value in attrs.items():
                if attr in self.graph[node1][node2]:
                    self.graph[node1][node2][attr] += value
                else:
                    self.graph[node1][node2][attr] = value
        else:
            self.graph.add_edge(node1, node2, **attrs)

    def size(self):
        return len(self.graph.nodes)

