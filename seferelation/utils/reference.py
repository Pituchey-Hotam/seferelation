from typing import Optional, Union, List, Tuple

import urllib


class Reference:
    def __init__(self, ref: str):
        self.ref = ref

    def to_sefaria_link(self) -> str:
        parsed_ref = "/" + self.ref
        parsed_ref = parsed_ref.replace(" ", "_")
        parsed_ref = urllib.parse.quote(parsed_ref)
        return urllib.parse.urlunparse(urllib.parse.ParseResult(
            scheme="https",
            netloc="www.sefaria.org.il",
            path=parsed_ref,
            params="", query="", fragment=""
        ))

    @staticmethod
    def from_sefaria_link(link: str) -> "Reference":
        link = urllib.parse.unquote(link)
        path = urllib.parse.urlparse(link).path
        path = path.replace("_", " ")
        path = path.replace("/", "")
        return Reference(path)

    def is_flat(self) -> bool:
        return "-" not in self.ref

    def is_range(self) -> bool:
        return self.get_range() != None

    def make_flat(self) -> "Reference":
        if "-" in self.ref:
            return Reference(self.ref[:self.ref.rfind(":")])
        return Reference(self.ref)

    def get_range(self) -> Optional[Tuple[int, int]]:
        # TODO: handle refs like ref 1:1-2:10
        try:
            start, end = self.ref[self.ref.rfind(":") + 1:].split("-")
            return int(start), int(end)
        except ValueError:
            return None

    def extract_range(self) -> List["Reference"]:
        flat = self.make_flat()
        ref_range = self.get_range()
        if not ref_range:
            return [flat]
        return [Reference(flat + str(i)) for i in range(*ref_range)]

    def is_in_range(self, ref_range: Union[str, "Reference"]) -> bool:
        # import ipdb; ipdb.set_trace()
        if not isinstance(ref_range, Reference):
            ref_range = Reference(ref_range)
        if not ref_range.is_range():
            return False
        if not self.ref.startswith(ref_range.make_flat().ref):
            return False
        range_start, range_end = ref_range.get_range()
        if self.is_range():
            start, end = self.get_range()
        else:
            start = end = int(self.ref.split(":")[-1])
        if (
            range_start <= start <= range_end and
            range_start <= end <= range_end
        ):
            return True
        return False

    def __hash__(self):
        return hash(self.ref)

