#Copyright STACKEO - INRIA 2020 .
from Stkml.Stkml.LayerElement.Component import Component


class PhyicalComponent(Component):

    def __init__(self, id_: str, c_type: str) -> object:
        super().__init__(id_=id_, type_=c_type)
        self.value = None
