from typing import Optional, Union, List, Tuple

import re
import urllib


def _str_replace_range(
    string: str, find: str, replace: str, start:int=None, end:int=None
) -> str:
    start = start or 0
    end = end or len(string)
    return string[:start] + string[start:end].replace(find, replace) + string[end:]


class Reference:
    def __init__(self, ref: str):
        self.ref = ref

    def to_sefaria_link(self) -> str:
        parsed_ref = "/" + self.ref
        number_idx = re.search(r'\d', parsed_ref)
        if number_idx != None:
            parsed_ref = _str_replace_range(parsed_ref, " ", ".", start=number_idx.start() - 1)
            parsed_ref = _str_replace_range(parsed_ref, ":", ".", start=number_idx.start())
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
        number_idx = re.search(r'\d', path)
        if number_idx != None:
            path = _str_replace_range(path, ".", ":", start=number_idx.start())
        path = path.replace(".", " ")
        path = path.replace("/", "")
        return Reference(path)

    def is_flat(self) -> bool:
        return "-" not in self.ref

    def is_range(self) -> bool:
        return self.get_range() != None

    def make_flat(self) -> "Reference":
        if "-" not in self.ref:
            return Reference(self.ref)
        if ":" in self.ref:
            return Reference(self.ref[:self.ref.rfind(":")])
        else:
            return Reference(self.ref[:self.ref.rfind(" ")])

    def parent(self) -> "Reference":
        return Reference(self.ref.split(":")[0])

    def get_range(self) -> Optional[Tuple[int, int]]:
        # TODO: handle refs like ref 1:1-2:10
        try:
            if ":" in self.ref:
                split_point = self.ref.rfind(":")
            elif " " in self.ref:
                split_point = self.ref.rfind(" ")
            else:
                return None
            start, end = self.ref[split_point + 1:].split("-")
            return int(start), int(end)
        except ValueError:
            return None

    def extract_range(self) -> List["Reference"]:
        flat = self.make_flat()
        ref_range = self.get_range()
        if not ref_range:
            return [flat]
        return [Reference(flat.ref + str(i)) for i in range(*ref_range)]

    def is_in_range(self, ref_range: Union[str, "Reference"]) -> bool:
        # import ipdb; ipdb.set_trace()
        if not isinstance(ref_range, Reference):
            ref_range = Reference(ref_range)
        if not ref_range.is_range():
            return self.parent() == ref_range
        if not self.ref.startswith(ref_range.make_flat().ref):
            return False
        range_start, range_end = ref_range.get_range()
        if self.is_range():
            start, end = self.get_range()
        elif ":" in self.ref:
            start = end = int(self.ref.split(":")[-1])
        else:
            start = end = int(self.ref.split(" ")[-1])
        if (
            range_start <= start <= range_end and
            range_start <= end <= range_end
        ):
            return True
        return False

    def __eq__(self, other: Union[str, "Reference"]) -> bool:
        if isinstance(other, str):
            return self.ref == other
        return self.ref == other.ref

    def __hash__(self):
        return hash(self.ref)

