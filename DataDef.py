import sys
from typing import TypeVar, Generic, List, IO, TextIO, cast, Tuple, NamedTuple

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
TXT = str
POS = str
POSTag = str
TERM = str
FACT = str
ABBR = str
TXT2 = str
TXT3 = str
CHUNK = str
CHUNKNPS = str

#
#   @data types
#
# @semanticbeeng @todo static typing; @data is PosFact same as POS ?
FactT = NamedTuple('Fact', [('start', int), ('end', int), ('string', str)])

AbbrT = NamedTuple("Abbr", [('begin', int), ('end', int), ('out_string', str), ('out_type', str), ('one_off', bool)])

#              confidence, term,  keep, classification,   rating, well_formedness_score, rank_score, webscore,  combined_score
ScoreT = Tuple[float,      str,   bool, POSTag,           str,    float,                 float,      float,     float]

PosWordT = NamedTuple('WordPosT', [('pos', str), ('word', POSTag)])
ChunkT = NamedTuple('ChunkT', [('term', str), ('positions', List[PosWordT])])


class File(Generic[DT]):
    def __init__(self, name: str) -> None:
        self.name = name

    def get(self) -> str:
        return self.name  # + '.' + DT

    def openText(self, mode: str = 'r', encoding=None, errors=None) -> TextIO:
        return cast(TextIO, open(self.name, mode=mode, encoding=encoding, errors=errors))

    def openBin(self, mode: str = 'r') -> IO[bytes]:
        return cast(IO[bytes], open(self.name, mode=mode + 'b'))

def main(args: List[str]):
    posFile1 = File[POS]("123.pos")
    termsFile2 = File[TERM]("123.terms")

    posFile1 = termsFile2
    pos = List[POS]
    terms = List[TERM]

    pos = terms


if __name__ == '__main__': sys.exit(main(sys.argv))
