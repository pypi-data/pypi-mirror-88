#Copyright STACKEO - INRIA 2020 .
class Data:

    def __init__(self, size: float, size_unit: str, type_: str, reference: str):
        self.size = {size: size_unit}
        self.type = type_
        self.reference = reference
