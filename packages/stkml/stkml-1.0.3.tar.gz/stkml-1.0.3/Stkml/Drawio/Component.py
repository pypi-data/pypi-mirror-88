#Copyright STACKEO - INRIA 2020 .
import uuid


class Component:

    def __init__(self, name: str, type_: str):
        self.id = uuid.uuid1()
        self.name = name
        self.type = type_
        self.position = [10, 7]
        self.dimension = [240, 35] #90
