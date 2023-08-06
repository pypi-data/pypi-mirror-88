#Copyright STACKEO - INRIA 2020 .
from diagrams import Node

class Diagramlayer(Node):

    def __init__(self, label: str, height: int = 1):
        self.style = None
        self.shape = "plaintext"
        self.width = 2.5
        self.height = height
        if label == '':
            self.style = 'invis'
        super().__init__(label)
        padding = 0.1 * self.height

        self.attrs = {
            "shape": self.shape,
            "style": self.style,
            "width": str(self.width),
            "height": str(padding)
        }
        self.set_format_rules_on_parent()

    def set_format_rules_on_parent(self):
        if self._cluster:
            self._cluster.node(self._id, self.label, **self.attrs)
        else:
            self._diagram.node(self._id, self.label, **self.attrs)
