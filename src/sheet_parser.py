# Observability imports
import ipdb
import networkx as nx
#######################

from typing import List, Dict

import math
import itertools

import logger
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


def _is_ref_range(ref: str) -> bool:
    return "-" in ref


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


def _sheet_popularity(sheet: Dict):
    views = sheet.get("views")
    return int(math.log(views, 10))


class SheetParser:
    def __init__(self):
        self.graph = Graph()

    def _link_range_ref(self, ref: str):
        self.graph.add_node_type(ref, node_type="range")
        for r in _extract_refs_range(ref):
            self.graph.add_edge(ref, r)

    def _link_refs(self, n1, n2, **attrs):
        self.graph.add_edge(n1, n2, **attrs)
        if _is_ref_range(n1):
            self._link_range_ref(n1)
        if _is_ref_range(n2):
            self._link_range_ref(n2)

    def _add_full_graph_edges(self, nodes, popularity):
        nodes = set(nodes)
        if len(nodes) > 14:
            logger.log(f"too much nodes, pass it. nodes: {len(nodes)}, popularity: {popularity}")
            return
        for n1, n2 in itertools.combinations(nodes, 2):
            self._link_refs(n1, n2, sefaria_popularity=popularity)

    def add_sefaria_sheet_connections(self, sheet: Dict):
        refs = _extract_ref_from_sheet(sheet)
        popularity = _sheet_popularity(sheet)
        if popularity > 0:
            self._add_full_graph_edges(refs, popularity=popularity)
        return self.graph.size()

    def update_with_sheet_list(self, sheets: List[Dict]):
        for sheet in sheets:
            if not is_valid_sheet(sheet):
                continue
            size = self.add_sefaria_sheet_connections(sheet)
        logger.log(f"graph size: {size}")
        logger.log(f"connected_components: {nx.number_connected_components(self.graph.graph)}")

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

