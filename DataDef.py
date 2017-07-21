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
POS = str
TERM = str
ABBR = str
TXT2 = str
TXT3 = str
CHUNK = str

#
#   @data types
#
# @semanticbeeng @todo static typing; @data is PosFact same as POS ?
PosFact = NamedTuple('PosFact', [('start', int), ('end', int), ('string', str)])

Abbr = NamedTuple("Abbr",  [('begin', int), ('end', int), ('out_string', str), ('out_type', str), ('one_off', bool)])

#              confidence, term,  keep, classification,   rating, well_formedness_score, rank_score, webscore,  combined_score
ScoreT = Tuple[float,      str,   bool, str,              str,    float,                 float,      float,     float]

WordPosT = NamedTuple('WordPosT', [('word', str), ('pos', str)])
ChunkT = NamedTuple('ChunkT',   [('term', str), ('positions', List[WordPosT])])


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
