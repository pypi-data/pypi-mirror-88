#Copyright STACKEO - INRIA 2020 .
import uuid

from Stkml.Drawio.Component import Component


class Layer:
    def __init__(self, type_: str, hub: bool):
        self.type = type_
        self.hub = hub
        self.ids = []
        self.position = [10, 27, {'Service': 5, 'Data': -2,
                                  'Messaging': 13, 'Connectivity': 16,
                                  'Network': 7, 'Physical': 7,
                                  'Business': 8, 'Energy': 4}[
                                   self.type.split('layerElement')[0]]]
                                  # layer position (x,y) and label x absis
        self.colors = [{'Service': '6ED7D3', 'Data': '3CAEA3', 'Messaging': '2A9187', 'Connectivity': '5937AE',
                                  'Network': '6D41DA', 'Physical': 'B281FF', 'Business': 'F8CECC', 'Energy': 'F8CECC'}
                       [self.type.split('layerElement')[0]],
                        'none']
        self.dimension = [280, 60]
        self.components = []
        self.hatching = False
        self.generate_ids()

    def generate_ids(self) -> None:
        for _ in range(4):
            self.ids.append(uuid.uuid1())

    def add_component(self, name: str, type_: str) -> Component:
        if self.colors[0] == 'FFFFFF':
            self.colors[0] = 'D5E8D4'
        component = Component(name, type_)
        self.set_component_position(component)
        self.components.append(component)
        return component

    def set_component_position(self, component):
        if self.hub:

            component.dimension[0] = self.dimension[0] / 2 - 16
            component.position[0] += (component.dimension[0] + 10) * len(self.components) - 8
            #c.position[0] += c.dimension[0] * len(self.components) + 10
        else:
            #component.position[0] = 0
            component.position[1] += component.dimension[1] * len(self.components) + (len(self.components) + 1) * 10
            component.dimension[1] = self.dimension[1] - 25
            component.dimension[0] = self.dimension[0] - 40
            if len(self.components) > 0:
                self.dimension[1] += component.dimension[1] + 10

    def __len__(self) -> int:
        return len(self.components)

    def set_blank(self) -> None:
        self.colors[0] = 'FFFFFF'
        self.colors[1] = '999999'

    def hachting(self) -> None:
        #self.colors[0] = 'D5DDE5'
        colors = {'Service': '60cac6', 'Data': '2fa499', 'Messaging': '1e897f', 'Connectivity': '5332a9',
                                  'Network': '663bd3', 'Physical': 'a777f4', 'Business': 'F8CECC', 'Energy': 'e9c0be'}
        self.hatching = colors[self.type.split('layerElement')[0]]

    def update_height(self, new_height):
        self.dimension[1] = new_height
        if len(self.components) > 0:
            last_comp = self.components[-1]
            dim = last_comp.dimension[1] + last_comp.position[1]
            if self.dimension[1] - dim > 20:
                for comp in self.components:
                    comp.dimension[1] = self.dimension[1] - 25
