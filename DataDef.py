from typing import TypeVar, Generic

# @resource https://www.python.org/dev/peps/pep-0484/#user-defined-generic-types

DT = TypeVar('DT')

class LoggedVar(Generic[DT]):
    def __init__(self, value: DT, name: str) -> None:
        self.name = name
        self.value = value

    def get(self) -> DT:
        return self.value

POS = str
TERMS = str
ABBR = str

class FileName(Generic[DT]):
    def __init__(self, value: DT) -> None:
        self.value = value

    def get(self) -> DT:
        return self.value

posFile1 = FileName[POS]("123.pos")
termsFile2 = FileName[TERMS]("123.terms")

posFile1 = termsFile2