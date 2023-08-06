#Copyright STACKEO - INRIA 2020 .
import os

from diagrams import Node

class DiagramNode(Node):

    def __init__(self, icon, label, quantity=0):
        self._icon_dir = os.path.dirname(icon)
        self._icon = os.path.basename(icon)
        self.label = label
        if quantity and quantity > 1:
            self.label = f'{quantity}\n{self.label}'
        super().__init__(self.label)
