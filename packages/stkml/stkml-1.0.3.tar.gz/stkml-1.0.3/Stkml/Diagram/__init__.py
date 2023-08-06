#Copyright STACKEO - INRIA 2020 .



from Stkml.Diagram.Graphviz.LayerDiagram import LayerDiagram
from Stkml.Diagram.Graphviz.RegionDiagram import RegionDiagram
from Stkml.Diagram.Graphviz.SystemDiagram import SystemDiagram
from Stkml.Diagram.Graphviz.Node import DiagramNode
from Stkml.Diagram.Graphviz.Layer import Diagramlayer
from Stkml.Diagram.Map.NodeMarker import NodeMarker
from Stkml.Diagram.Map.TopologyMap import TopologyMap
from Stkml.Stkml import Stkml


class StkmlDiagram:

    def __init__(self):
        self.diagram_attr = {"pad": "0.2", "splines": "ortho", "nodesep": "0.6",
                             "ranksep": "1", "fontname": "Sans-Serif", "fontsize": "15", "fontcolor": "#2D3436"}

        self.funcs = {1: SystemDiagram, 2: RegionDiagram, 3: TopologyMap}

    def diagram_from_stkml(self, type_: int, stkml: Stkml, output: str) -> str:
        bound = self.funcs[type_](self.diagram_attr)
        return bound.from_stackml(stkml, output)
