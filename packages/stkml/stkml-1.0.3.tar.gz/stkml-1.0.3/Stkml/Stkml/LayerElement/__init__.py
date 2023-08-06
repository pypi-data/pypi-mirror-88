#Copyright STACKEO - INRIA 2020 .
from Stkml.Stkml.LayerElement.Component import Component


class LayerElement:

    def __init__(self, name: str, type_: str, hub):
        self.name = name
        self.type = type_
        self.function = None
        self.provider = None
        if hub == 'Hub':
            self.hub = True
        else:
            self.hub = False
        self.components = []

    def set_function(self, function: str) -> None:
        self.function = function

    def set_provider(self, provider: str) -> None:
        self.provider = provider

    def add_component(self, component) -> None:
        self.components.append(component)

    def set_components(self, components) -> None:
        for component in components:
            self.add_component(Component(id_=component.get('name'), type_=component.get('nature')))

    def __len__(self):
        return 1 if self.hub else len(self.components)
