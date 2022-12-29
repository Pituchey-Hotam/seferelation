# Observability imports
import ipdb
import networkx as nx
#######################

from typing import List, Dict

import itertools

from graph_manager import Graph


def is_valid_sheet(sheet: Dict):
    if not isinstance(sheet, Dict):
        return False
    if "sources" not in sheet:
        return False
    return True


def _extract_ref_from_sheet(sheet: Dict):
    sources = sheet["sources"]
    refs = [s["ref"] for s in sources if "ref" in s and s["ref"]]
    return refs


def _is_flat_ref(ref: str) -> bool:
    return "-" not in ref


def _flat_ref(ref: str):
    if "-" in ref:
        return ref[:ref.rfind(":")]
    return ref


def _ref_range(ref: str):
    try:
        start, end = ref[ref.rfind(":"):].split("-")
        return int(start), int(end)
    except Exception:
        return None


def _extract_refs_range(ref: str) -> List[str]:
    flat = _flat_ref(ref)
    ref_range = _ref_range(ref)
    if not ref_range:
        return [flat]
    return [flat + str(i) for i in range(*ref_range)]


def _flat_refs(refs: List[str]):
    return [_flat_ref(ref) for ref in refs]


def _sheet_score(sheet: Dict):
    views = sheet.get("views")
    if views < 10:
        return 0
    elif views < 100:
        return 1
    elif views < 1000:
        return 2
    else:
        return 3


class SheetParser:
    def __init__(self):
        self.graph = Graph()

    def _link_refs(self, n1, n2, weight):
        self.graph.add_edge(n1, n2, weight)
        if not _is_flat_ref(n1):
            for r in _extract_refs_range(n1):
                self.graph.add_edge(n1, r, weight * 0.1)
        if not _is_flat_ref(n2):
            for r in _extract_refs_range(n2):
                self.graph.add_edge(n2, r, weight * 0.1)

    def _add_full_graph_edges(self, nodes, weight=None):
        nodes = set(nodes)
        if len(nodes) > 12:
            print(f"too much nodes, pass it. nodes: {len(nodes)}")
            return
        for n1, n2 in itertools.combinations(nodes, 2):
            self._link_refs(n1, n2, weight)

    def add_sefaria_sheet_connections(self, sheet: Dict):
        refs = _extract_ref_from_sheet(sheet)
        # refs = _flat_refs(refs)
        score = _sheet_score(sheet)
        if score > 0:
            self._add_full_graph_edges(refs, weight=1 / score)
        return self.graph.size()

    def update_with_sheet_list(self, sheets: List[Dict]):
        for sheet in sheets:
            if not is_valid_sheet(sheet):
                continue
            size = self.add_sefaria_sheet_connections(sheet)
        print(f"graph size: {size}")
        print(f"connected_components: {nx.number_connected_components(self.graph.graph)}")

    def find_relations_of(self, ref: str) -> List:
        nx_graph = self.graph.graph
        if not ref in nx_graph:
            return []
        relations_by_distance = nx.single_source_shortest_path_length(
            nx_graph, ref, cutoff=1.2
        )
        relations = sorted(
            relations_by_distance, key=lambda r: relations_by_distance[r]
        )
        return list(relations)

