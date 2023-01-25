# Observability imports
import ipdb
import networkx as nx
#######################

from typing import List, Dict, Set

import math
import itertools

from seferelation import logger
from seferelation.utils.reference import Reference
from seferelation.graph_manager import Graph


def is_valid_sheet(sheet: Dict):
    if not isinstance(sheet, Dict):
        return False
    if "sources" not in sheet:
        return False
    return True


def _extract_ref_from_sheet(sheet: Dict) -> Set[Reference]:
    sources = sheet["sources"]
    refs = set([Reference(s["ref"]) for s in sources if "ref" in s and s["ref"]])
    return refs


def _sheet_popularity(sheet: Dict):
    views = sheet.get("views", 0)
    return int(math.log(views, 10))


class SheetParser:
    def __init__(self):
        self.graph = Graph()

    def _link_range_ref(self, ref: Reference):
        self.graph.add_node_type(ref.ref, node_type="range")
        for r in ref.extract_range():
            self.graph.add_edge(ref.ref, r.ref)

    def _link_refs(self, n1, n2, **attrs):
        self.graph.add_edge(n1.ref, n2.ref, **attrs)
        if n1.is_range():
            self._link_range_ref(n1)
        if n2.is_range():
            self._link_range_ref(n2)

    def _add_full_graph_edges(self, nodes, popularity):
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
        if ref not in nx_graph:
            return []
        neighbors = [(other, nx_graph[ref][other].get("sefaria_popularity", 0)) for other in nx_graph.neighbors(ref)]
        my_ranges = filter(lambda _range: Reference(ref).is_in_range(_range[0]), neighbors)
        for _range in my_ranges:
            print(_range)
            neighbors += [(other, nx_graph[_range][other].get("sefaria_popularity", 0)) for other in nx_graph.neighbors(_range)]
        return list(sorted(
            neighbors,
            key=lambda neighbor: neighbor[1],
            reverse=True,
        ))

    def _find_relations_by_distance(self, ref: str) -> List:
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

