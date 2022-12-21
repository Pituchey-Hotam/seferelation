from typing import List

import itertools

from .graph_manager import Graph


def _extract_ref_from_sheet(sheet: Dict):
    sources = response["sources"]
    refs = [s["ref"] for s in sources if "ref" in s]
    return refs


def _flat_ref(ref: str):
    if "-" in ref:
        return ref[:ref.rfind(":")]
    return ref


def _flat_refs(refs: List[str]):
    return [_flat_ref(ref) for ref in refs)


class SheetParser:
    def __init__(self):
        self.graph = Graph()

    def _add_full_graph_edges(self, nodes):
        nodes = set(nodes)
        if len(nodes) > 12:
            print("too much nodes, pass it")
            return
        for n1, n2 in itertools.combinations(nodes, 2):
            self.graph.add_edge(self.graph.node(n1), self.graph.node(n2))

    def add_sefaria_sheet_connections(self, sheet: Dict):
        refs = _extract_ref_from_sheet(sheet)
        refs = _flat_refs(refs)
        
