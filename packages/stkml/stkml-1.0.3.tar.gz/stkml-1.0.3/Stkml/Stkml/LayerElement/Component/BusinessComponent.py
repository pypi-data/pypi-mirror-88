#Copyright STACKEO - INRIA 2020 .
from Stkml.Stkml.LayerElement.Component import Component


class BusinessComponent(Component):

    def __init__(self, id_: str, c_type: str, type_: str):
        super().__init__(id_=id_, type_=c_type)
        self.type = type_
        self.period = None
        self.value = None
        self.unit = None

    def set_value(self, value: float) -> None:
        self.value = value

    def set_unit(self, unit: str):
        self.unit = unit

    def set_period(self, period: str) -> None:
        self.period = period
