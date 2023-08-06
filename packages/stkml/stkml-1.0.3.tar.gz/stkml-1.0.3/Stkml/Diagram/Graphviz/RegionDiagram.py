#Copyright STACKEO - INRIA 2020 .
# pylint: disable=pointless-statement

from diagrams import Diagram, Cluster, Edge

from Stkml.Diagram.Graphviz.Node import DiagramNode
from Stkml.Diagram.Graphviz import Graphviz
from Stkml.Diagram.Graphviz.GraphvizManger import GraphvizManger
from Stkml.Stkml import Stkml


class RegionDiagram(Graphviz):

    def __init__(self,diagram_attr: dict):
        super().__init__(diagram_attr=diagram_attr)

    def from_stackml(self, stackml: Stkml, output: str) -> str:
        nodes = {}
        with GraphvizManger() as graphviz_manager:
            with Diagram(stackml.topology.name, filename=output, show=False, graph_attr=self.diagram_attr):
                with Cluster(stackml.topology.name):
                    for region in stackml.regions:
                        nodes[region.name] = {}
                        with Cluster(region.name):
                            for node in region.nodes:
                                _icon = stackml.get_node(node).icon
                                d_node = DiagramNode(_icon, node, region.nodes[node])
                                nodes[region.name][node] = d_node
                    self.create_regions_links(nodes, stackml.links)
        return graphviz_manager

    def create_regions_links(self, nodes, links):
        linked = []
        for node in nodes:
            #region local links
            sources = []
            for link in links:
                if link.source not in sources:
                    node_source = nodes[node].get(link.source)
                    node_sink = nodes[node].get(link.sink)
                    if node_source and node_sink:
                        sources.append(link.source)
                        linked.append(link.source)
                        edge = Edge(color="black")
                        node_source >> edge << node_sink
        # links between regions
        for link in links:
            if link.source not in linked:
                linked.append(link.source)
                nodes_source = self.get_all_nodes(nodes, link.source)
                nodes_sink = self.get_all_nodes(nodes, link.sink)
                for n_src in nodes_source:
                    for n_sink in nodes_sink:
                        edge = Edge(color="black")
                        n_src >> edge << n_sink
    @staticmethod
    def get_all_nodes(nodes, name):
        nodes_ = []
        for node in nodes:
            region = nodes[node]
            for node_ in region:
                if node_ == name:
                    nodes_.append(region[node_])
        return nodes_
