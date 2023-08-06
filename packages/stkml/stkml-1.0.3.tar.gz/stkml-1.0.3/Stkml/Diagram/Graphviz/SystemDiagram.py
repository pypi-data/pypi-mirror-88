#Copyright STACKEO - INRIA 2020 .
# pylint: disable=pointless-statement

from diagrams import Diagram, Cluster, Edge
from Stkml.Diagram.Graphviz.GraphvizManger import GraphvizManger
from Stkml.Diagram.Graphviz import Graphviz
from Stkml.Stkml import Stkml
from Stkml.Diagram.Graphviz.Node import DiagramNode

class SystemDiagram(Graphviz):

    def __init__(self, diagram_attr: dict):
        super().__init__(diagram_attr=diagram_attr)

    def from_stackml(self, stackml: Stkml, output: str) -> str:
        nodes = {}
        with GraphvizManger() as graphviz_manager:
            with Diagram(stackml.topology.name, filename=output, show=False, graph_attr=self.diagram_attr):
                with Cluster(stackml.topology.name):

                    for tier in stackml.tiers:
                        tier_type = tier.type
                        with Cluster(tier_type):
                            for node in tier.nodes:
                                _icon = node.icon
                                d_node = DiagramNode(_icon, node.id_, quantity=node.cardinality)
                                nodes[node.id_] = d_node
                    sources = []
                    for link in stackml.links:
                        node_source = nodes.get(link.source)
                        node_sink = nodes.get(link.sink)
                        if node_source and node_sink:
                            if node_source not in sources:
                                sources.append(node_source)
                                edge = Edge(color="black")
                                node_source >> edge << node_sink
        return graphviz_manager
