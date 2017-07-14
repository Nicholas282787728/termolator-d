from typing import TypeVar, Generic, List
import sys

# @resource https://www.python.org/dev/peps/pep-0484/#user-defined-generic-types

DT = TypeVar('DT', contravariant=True)

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
TERMS = str
ABBR = str

class FileName(Generic[DT]):
    def __init__(self, name: DT) -> None:
        self.name = name

    # def get(self) -> DT:
    #     return self.name


def main(args: List[str]):
    posFile1 = FileName(POS("123.pos"))
    termsFile2 = FileName(TERMS("123.terms"))

    posFile1 = termsFile2
    pos = List[POS]
    terms = List[TERMS]

    pos = terms

if __name__ == '__main__': sys.exit(main(sys.argv))

