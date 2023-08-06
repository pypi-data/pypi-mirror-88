#Copyright STACKEO - INRIA 2020 .
import uuid

from Stkml.Drawio.Node import Node


class Tier:

    def __init__(self, name, type_):
        self.name = name
        self.ids = []
        self.nodes = []
        self.position = [20, 120]
        self.dimension = [300, 0]
        self.type = type_
        self.generate_ids()

    def generate_ids(self):
        for _ in range(4):
            self.ids.append(uuid.uuid1())

    def add_node(self, name: str, nature, icon=None, type_=None) -> Node:
        if not self.type:
            self.type = type_.split('Node')[0]
        node = Node(name, self.type + 'Node', nature)
        node.set_icon(icon)

        self.nodes.append(node)
        return node

    def generate_nodes_position_level2(self) -> None:
        i = 0
        height = 0
        width = 0
        for node in self.nodes:
            if node.stack:
                node.position.append(int((self.dimension[0] - node.dimension[0]) / 2))
                y_axis = self.position[1] - 40 + i * 20 + height
                node.position.append(y_axis)
                height += node.dimension[1]
                width = node.dimension[0]
                self.dimension[1] += node.dimension[1] + 20


            else:
                node.position.append(width + 20)
                y_axis = self.position[1] - 40
                node.position.append(y_axis)
                width += node.dimension[0]
                height = node.dimension[1]
                self.dimension[0] += node.dimension[0] + 20 #* (i - 1)
            i += 1

        #self.dimension[1] = height + 95
        #self.dimension[0] = width + 20 * (i - 1)

    def generate_nodes_position_level1(self) -> None:
        i = 0
        dim = 0
        for node in self.nodes:
            node.position.append(int((self.dimension[0] - node.dimension[0]) / 2))
            y_axis = self.position[1] - 40 + i * 40 + dim
            node.position.append(y_axis)
            dim += node.dimension[1]
            i += 1
        self.dimension[1] = dim + i * 40 + 95
