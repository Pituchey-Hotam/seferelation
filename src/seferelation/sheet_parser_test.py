import pytest

from seferelation import sheet_parser
from seferelation.utils.reference import Reference


@pytest.fixture
def popularity() -> int:
    return 1


@pytest.fixture
def parser_graph(popularity: int) -> sheet_parser.SheetParser:
    parser = sheet_parser.SheetParser()
    book1_nodes = [Reference(ref) for ref in ["book1 a", "book1 b", "book1 c"]]
    parser._add_full_graph_edges(book1_nodes, popularity)
    return parser


def test_sheet_parser_find_relations(
    parser_graph: sheet_parser.SheetParser,
):
    relations = parser_graph.find_relations_of("book1 a")
    relations = [r[0] for r in relations]
    assert relations == ["book1 b", "book1 c"]


