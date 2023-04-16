import pickle

from fastapi import FastAPI
from pathlib import Path

from seferelation.utils import Reference


app = FastAPI()


GRAPH_PATH = Path("sefaria_400k_graph_2023_01_03.pickle")


if GRAPH_PATH.exists():
    with GRAPH_PATH.open("rb") as f:
        graph = pickle.load(f)
    print(f"Loaded graph from {GRAPH_PATH}")
else:
    print(f"ERROR: graph not found at {GRAPH_PATH}")
    exit()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/relations")
def read_item(sefaria_link: str):
    ref = Reference.from_sefaria_link(sefaria_link)
    print(f"Sefaria ref is: {ref.ref}")
    relations = graph.find_relations_of(ref.ref)
    relations = [
        (Reference(rel).to_sefaria_link(), priority) for rel, priority
        in relations
    ]
    return {"relations": relations}

