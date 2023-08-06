#Copyright STACKEO - INRIA 2020 .

from Stkml.Stkml.LayerElement import LayerElement
from Stkml.Stkml.LayerElement.ConnectivitylayerElement import ConnectivitylayerElement
from Stkml.Stkml.LayerElement.DatalayerElement import DatalayerElement
from Stkml.Stkml.LayerElement.EnergylayerElement import EnergylayerElement
from Stkml.Stkml.LayerElement.MessaginglayerElement import MessaginglayerElement
from Stkml.Stkml.LayerElement.NetworklayerElement import NetworklayerElement
from Stkml.Stkml.LayerElement.PhysicallayerElement import PhysicallayerElement
from Stkml.Stkml.LayerElement.ServicelayerElement import ServicelayerElement
from Stkml.Stkml.LayerElement.BusinesslayerElement import BusinesslayerElement


class Node:

    def __init__(self, id_: str, cardinality: int, type_: str):
        self.id_ = id_
        self.cardinality = cardinality
        self.element_types = {'BusinesslayerElement': BusinesslayerElement,
                              'ServicelayerElement': ServicelayerElement,
                              'DatalayerElement': DatalayerElement,
                              'MessaginglayerElement': MessaginglayerElement,
                              'ConnectivitylayerElement': ConnectivitylayerElement,
                              'NetworklayerElement': NetworklayerElement,
                              'PhysicallayerElement': PhysicallayerElement,
                              'EnergylayerElement': EnergylayerElement}
        self.layers_element = []
        self.type = type_
        self.nature = ''
        self.icon = None

    def add_layer_element(self, element, type_, hub) -> LayerElement:
        layer_element = self.element_types[type_](element, hub)
        self.layers_element.append(layer_element)
        return layer_element

    def get_layer_element(self, type_: str):
        layer = None
        for layer_ in self.layers_element:
            if layer_.type == type_:
                layer = layer_
                break
        return layer

    def get_components(self, layer_type: str):
        components = None
        layer_elem = self.get_layer_element(layer_type)
        if layer_elem:
            components = layer_elem.components
        return components

    def set_nature(self, nature: str) -> None:
        self.nature = nature

    def set_icon(self, icon: str):
        self.icon = icon
