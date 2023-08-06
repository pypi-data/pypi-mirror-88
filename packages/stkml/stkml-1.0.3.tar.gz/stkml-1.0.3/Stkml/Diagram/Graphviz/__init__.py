#Copyright STACKEO - INRIA 2020 .
from abc import abstractmethod

from Stkml.Stkml import Stkml


class Graphviz:

    def __init__(self, diagram_attr: dict):
        self.diagram_attr = diagram_attr

    @abstractmethod
    def from_stackml(self, stackml: Stkml, output: str) -> str:
        return 'Ok'
