#Copyright STACKEO - INRIA 2020 .
from typing import List

from Stkml.Stkml.LayerElement.Component.DataComponent.Arg import Arg


class Job:

    def __init__(self, id_: str):
        self.id = id_
        self.prec = []
        self.state = 'Running'
        self.type = None
        self.args: List[Arg] = []

    def set_state(self, state: str) -> None:
        self.state = state

    def add_prec(self, prec: str) -> None:
        self.prec.append(prec)

    def set_type(self, type_: str) -> None:
        self.type = type_

    def add_arg(self, name: str, type_: str) -> Arg:
        arg = Arg(name, type_)
        self.args.append(arg)
        return arg
