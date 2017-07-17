import sys
from typing import TypeVar, Generic, List, IO, TextIO, cast

# @resource https://www.python.org/dev/peps/pep-0484/#user-defined-generic-types

DT = TypeVar('DT')  # , contravariant=True)

# class TP:
#     def __init__(self, v: str) -> None:
#         self.v = v
#
# class POS(TP):
#     pass
#
# class TERMS(TP):
#     pass
#
# class ABBR(TP):
#     pass
POS = str
TERM = str
ABBR = str
TXT2 = str
TXT3 = str

class File(Generic[DT]):
    def __init__(self, name: str) -> None:
        self.name = name

    def get(self) -> str:
        return self.name  # + '.' + DT

    def openText(self, mode: str = 'r') -> TextIO:
        return cast(TextIO, open(self.name, mode))

def main(args: List[str]):
    posFile1 = File[POS]("123.pos")
    termsFile2 = File[TERM]("123.terms")

    posFile1 = termsFile2
    pos = List[POS]
    terms = List[TERM]

    pos = terms


if __name__ == '__main__': sys.exit(main(sys.argv))
