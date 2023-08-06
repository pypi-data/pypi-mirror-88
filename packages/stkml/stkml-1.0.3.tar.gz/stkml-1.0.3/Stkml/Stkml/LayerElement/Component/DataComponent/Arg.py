#Copyright STACKEO - INRIA 2020 .
from typing import List

from Stkml.Stkml.LayerElement.Component.DataComponent.Data import Data


class Arg:

    def __init__(self, name: str, type_: str):
        self.name = name
        self.type = type_
        self.datas: List[Data] = []


    def add_data(self, size: float, size_unit: str, type_: str, reference: str) -> None:
        self.datas.append(Data(size, size_unit, type_, reference))
