from typing import Optional

import os
import sys
sys.path.append("/mnt/c/users/ykane/Documents/seferelation/seferelation")

from pathlib import Path
import pickle
from tqdm import tqdm

from seferelation.sheet_parser import SheetParser, is_valid_sheet
from seferelation.utils import Reference



SHEETS_PICKLE_PATH = Path("scrapper/downloads")
# SHEETS_PICKLE_PATH = Path("scrapper/sheets_sample_5percent.pickle")
GRAPH_PATH = Path("sefaria_400k_graph_2023_01_03.pickle")


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
            "debug": self._debug,
        }

    def _help(self):
        print("Help: \nUse one of the following commands:")
        for cmd in self.commands_map:
            print(cmd)
        print("exit")
        print()

    def _relations(self):
        ref = input("Enter a sefaria ref: ")
        ref = Reference.from_sefaria_link(ref)
        print(f"Sefaria ref is: {ref.ref}")
        relations = self.graph.find_relations_of(ref.ref)
        for i, rel in enumerate(relations):
            rel, priority = rel
            sefaria_link = Reference(rel).to_sefaria_link()
            print(f"{i:02}: ({priority:02}) {sefaria_link}")

    def _debug(self):
        print("debugging, use self.graph")
        import ipdb; ipdb.set_trace()

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
    print("hi2")
    if GRAPH_PATH.exists():
        with GRAPH_PATH.open("rb") as f:
            graph = pickle.load(f)
        print(f"Loaded graph from {GRAPH_PATH}")
    else:
        graph = build_graph(SHEETS_PICKLE_PATH, GRAPH_PATH)
    CLIQueryManager(graph).start()


if __name__ == "__main__":
    main()
