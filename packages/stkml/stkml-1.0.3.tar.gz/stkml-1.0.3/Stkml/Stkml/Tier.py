#Copyright STACKEO - INRIA 2020 .
import os

from Stkml import ICONS
from Stkml.Stkml.Node import Node


class Tier:

    def __init__(self, name: str, type_: str) -> object:
        self.name = name
        self.type = type_
        self.nodes = []

    def add_node(self, id_: str, cardinality: int, type_: str) -> Node:
        node = Node(id_=id_, cardinality=cardinality, type_=type_)
        self.nodes.append(node)
        return node
