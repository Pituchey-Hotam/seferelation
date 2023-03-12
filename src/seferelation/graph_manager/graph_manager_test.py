import pytest

from .graph_manager import Graph


def test_graph_node():
    g = Graph()
    assert g.node(0) == g.node(0)


def test_graph_edge():
    g = Graph()
    g.node(0)
    g.node(1)
    g.add_edge(0, 1)

