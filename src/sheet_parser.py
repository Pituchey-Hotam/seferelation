import ipdb
from typing import List, Dict

import itertools
import pickle

from graph_manager import Graph


def _extract_ref_from_sheet(sheet: Dict):
    sources = sheet["sources"]
    refs = [s["ref"] for s in sources if "ref" in s and s["ref"]]
    return refs


def _flat_ref(ref: str):
    if "-" in ref:
        return ref[:ref.rfind(":")]
    return ref


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

    def _add_full_graph_edges(self, nodes, weight=None):
        nodes = set(nodes)
        if len(nodes) > 12:
            print("too much nodes, pass it")
            return
        for n1, n2 in itertools.combinations(nodes, 2):
            self.graph.add_edge(self.graph.node(n1), self.graph.node(n2), weight)

    def add_sefaria_sheet_connections(self, sheet: Dict):
        ipdb.set_trace()
        refs = _extract_ref_from_sheet(sheet)
        refs = _flat_refs(refs)
        score = _sheet_score(sheet)
        self._add_full_graph_edges(refs, weight=score)
        return self.graph.size()


def main():
    PICKLE_PATH = "scrapper/sheets_sample_5percent.pickle"
    with open(PICKLE_PATH, 'rb') as f:
        sheets = pickle.load(f)
    sparser = SheetParser()

    for sheet in sheets[:100]:
        size = sparser.add_sefaria_sheet_connections(sheet)
        print(size)
    ipdb.set_trace()


if __name__ == "__main__":
    main()
