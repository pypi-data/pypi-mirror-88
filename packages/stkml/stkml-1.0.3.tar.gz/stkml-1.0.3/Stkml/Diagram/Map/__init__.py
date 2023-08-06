#Copyright STACKEO - INRIA 2020 .
from abc import abstractmethod

from Stkml.Stkml import Stkml


class RegionsMap:

    @abstractmethod
    def from_stackml(self, stackml: Stkml, output: str):
        pass
