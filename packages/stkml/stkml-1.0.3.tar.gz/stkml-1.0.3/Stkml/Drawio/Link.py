#Copyright STACKEO - INRIA 2020 .
import uuid

from Stkml.Drawio import Node


class Link:

    def __init__(self, source: Node, sink: Node, layer: str):
        self.id = uuid.uuid1()
        self.source = source
        self.sink = sink
        self.layer = layer
        self.display = True
        self.color = self.get_color()
        self.internal = self.is_internal()

    def is_internal(self):
        if self.source.type == self.sink.type:
            return True
        return False

    def get_color(self) -> str:
        colors = {'Service': '#2A9187',
                      'Data': '#2A9187',
                      'Messaging': '#2A9187',
                      'Connectivity': '#5937AE',
                      'Network': '#6D41DA',
                      'Physical': '#263239',
                      'Business': '#FD5501'}
        if self.layer:
            return colors[self.layer]
        return '#000000'
