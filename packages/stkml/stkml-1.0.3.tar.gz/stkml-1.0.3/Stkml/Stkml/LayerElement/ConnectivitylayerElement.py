#Copyright STACKEO - INRIA 2020 .
from Stkml.Stkml.LayerElement import LayerElement


class ConnectivitylayerElement(LayerElement):

    def __init__(self, name: str, hub):
        super().__init__(name, type(self).__name__, hub)
