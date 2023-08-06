#Copyright STACKEO - INRIA 2020 .
# pylint: disable=too-many-instance-attributes

import os
import uuid
import base64

import mimetypes

from Stkml.Drawio.Layer import Layer


class Node:

    def __init__(self, name, type_, nature):
        self.name = name
        self.ids = []
        self.position = []
        self.dimension = [0, 0]
        self.image = None
        self.type = type_
        self.layers = []
        self.generate_ids()
        self.box_style = self.set_box_style(nature)
        self.stack = True
        self.icon = None

    def generate_ids(self):
        for _ in range(3):
            self.ids.append(uuid.uuid1())

    def set_icon(self, icon):
        self.icon = icon

    def generate_icon_uri(self):
        """Convert a file (specified by a path) into a data URI."""
        if not os.path.exists(self.icon):
            raise FileNotFoundError
        mime, _ = mimetypes.guess_type(self.icon)
        with open(self.icon, 'rb') as img:
            data = img.read()
            data64 = base64.b64encode(data)
            self.image = f'data:{mime},{data64.decode()}'

    def get_layer(self, layer: str) -> Layer:
        layer_ = None
        for node_layer in self.layers:
            if node_layer.type == layer:
                layer_ = node_layer
                break
        return layer_

    def add_layer(self, type_: str, hub=False) -> Layer:
        layer = Layer(type_, hub)
        self.layers.append(layer)
        return layer

    def generate_layers_position(self):
        for i_l in range(1, len(self.layers)):
            self.layers[i_l].position[1] = self.layers[i_l - 1].position[1] + self.layers[i_l - 1].dimension[1] + 10

    def set_dimensions(self):
        self.dimension[0] = 300 #self.layers[-1].dimension[0] + 20
        self.dimension[1] = self.layers[-1].position[1] + self.layers[-1].dimension[1] + 10

    def set_box_style(self, nature) -> str:
        box_style = ''
        if nature != 'Hardware':
            box_style = "dashed=1;"
        if nature == 'Service':

            box_style = f'{box_style}dashPattern=1 4;'
        return box_style

    def un_stack(self):
        self.stack = False
