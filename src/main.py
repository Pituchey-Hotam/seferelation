from typing import Optional

import os

from pathlib import Path
import pickle
from tqdm import tqdm

from sheet_parser import SheetParser, is_valid_sheet


GRAPH_PATH = Path("sefaria_400k_graph.pickle")


def _build_graph_old_impl(sheets_pickle_path: Path, out_graph_path: Path):
    with open(sheets_pickle_path, 'rb') as f:
        sheets = pickle.load(f)
    print("Loaded sheets")
    sparser = SheetParser()

    connected_components = []
    i = 0
    for sheet in sheets:
        if not is_valid_sheet(sheet):
            continue
        size = sparser.add_sefaria_sheet_connections(sheet)
        print(size)
        i += 1
        if i % 1000 == 0:
            connected_components.append(nx.number_connected_components(sparser.graph.graph))
            print(f"connected_components: {connected_components[-1]}")
    connected_components.append(nx.number_connected_components(sparser.graph.graph))
    print(f"connected_components: {connected_components}")
    with open(out_graph_path, "wb") as f:
        pickle.dump(sparser, f)
    print(f"Saved graph to {out_graph_path}")
    return sparser


def build_graph(sheets_pickle_path: Path, out_graph_path: Path):
    sparser = SheetParser()
    if sheets_pickle_path.is_dir():
        sheet_paths = [sheets_pickle_path / name for name in os.listdir(sheets_pickle_path)]
    else:
        sheet_paths = [sheets_pickle_path]
    for sheet_path in tqdm(sheet_paths):
        with sheet_path.open("rb") as f:
            sheets = pickle.load(f)
        sparser.update_with_sheet_list(sheets)
    with open(out_graph_path, "wb") as f:
        pickle.dump(sparser, f)
    print(f"Saved graph to {out_graph_path}")
    return sparser


class CLIQueryManager:
    def __init__(self, graph):
        self.graph = graph
        self.commands_map = {
            "help": self._help,
            "relations": self._relations,
        }

    def _help(self):
        print("Help: \nUse one of the following commands:")
        for cmd in self.commands_map:
            print(cmd)
        print("exit")
        print()

    def _relations(self):
        ref = input("Enter a sefaria ref: ")
        relations = self.graph.find_relations_of(ref)
        for rel in relations:
            print(rel)

    def start(self):
        cmd = input("Command: ")
        while cmd != "exit":
            if cmd not in self.commands_map:
                self._help()
            else:
                self.commands_map[cmd]()
            cmd = input("Command: ")
        print("exiting")


def main():
    print("hi")
    SHEETS_PICKLE_PATH = Path("scrapper/downloads")
    # SHEETS_PICKLE_PATH = Path("scrapper/sheets_sample_5percent.pickle")
    if GRAPH_PATH.exists():
        with GRAPH_PATH.open("rb") as f:
            graph = pickle.load(f)
        print(f"Loaded graph from {GRAPH_PATH}")
    else:
        graph = build_graph(SHEETS_PICKLE_PATH, GRAPH_PATH)
    CLIQueryManager(graph).start()


if __name__ == "__main__":
    main()
