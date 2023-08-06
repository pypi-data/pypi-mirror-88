#Copyright STACKEO - INRIA 2020 .
class Region:

    def __init__(self, name: str, type_: str):
        self.name = name
        self.type = type_
        self.nodes = {} # {node_id : number}

    def add_node(self, node_id: str, number: int) -> None:
        self.nodes[node_id] = number
