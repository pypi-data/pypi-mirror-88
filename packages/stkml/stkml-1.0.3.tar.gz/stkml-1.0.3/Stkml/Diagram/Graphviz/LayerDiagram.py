#Copyright STACKEO - INRIA 2020 .
# pylint: disable=pointless-statement

from diagrams import Diagram, Cluster, Edge

from Stkml.Diagram.Graphviz.Layer import Diagramlayer
from Stkml.Diagram.Graphviz import Graphviz
from Stkml.Diagram.Graphviz.GraphvizManger import GraphvizManger
from Stkml.Stkml import Stkml, Link


class LayerDiagram(Graphviz):

    def __init__(self, diagram_attr: dict):
        super().__init__(diagram_attr=diagram_attr)
        self.layer_types = {'ServicelayerElement': 'Service',
                            'DatalayerElement': 'Data',
                            'MessaginglayerElement': 'Messaging',
                            'ConnectivitylayerElement': 'Connectivity',
                            'NetworklayerElement': 'Network',
                            'PhysicallayerElement': 'Physical',
                            'BusinesslayerElement': 'Business'
                            }
        self.layer_style = {"style": "dashed", "bgcolor": "#A8EEEB", "labeljust": "r", "fontsize": "9", "margin": "15"}

    def from_stackml(self, stackml: Stkml, output: str) -> str:
        layer_max_nb_cmp = []
        for layer_type in self.layer_types:
            layer_max_nb_cmp.append(self.get_layer_max_nb_components(stackml, layer_type))
        layers = {}  # { Node:{layers} }
        with GraphvizManger() as graohviz_manager:
            with Diagram(stackml.topology.name, filename=output, show=False, graph_attr=self.diagram_attr):
                with Cluster(stackml.topology.name, graph_attr={"style": "", "bgcolor": "White"}):
                    for tier in stackml.tiers:
                        with Cluster(tier.name, graph_attr={"style": "", "bgcolor": "White", "labeljust": "r"}):
                            node = tier.nodes[0]
                            layers[node.id_] = {}
                            with Cluster(node.id_, graph_attr={"style": "", "bgcolor": "#6ED7D3"}):
                                for layer_, nb_cmp in zip(self.layer_types, layer_max_nb_cmp):
                                    layer = node.get_layer_element(layer_)
                                    layer_name = f'<<I> {self.layer_types[layer_]} </I>>'
                                    d_layer = self.create_layer(layer, layer_name, nb_cmp)
                                    if d_layer:
                                        layers[node.id_][self.layer_types[layer_]] = d_layer
                    for link in stackml.links:
                        self.create_layer_link(layers, link)
        return graohviz_manager

    def get_layer_max_nb_components(self, stackml, layer) -> int:
        max_nb = 0
        tiers = stackml.tiers
        for tier in tiers:
            for node in tier.nodes:
                layer_elem = node.get_layer_element(layer)
                if layer_elem:
                    max_nb = max(max_nb, len(layer_elem))
        return max_nb

    def create_layer_link(self, layers: dict, link: Link) -> None:
        layer_src = layers.get(link.source)
        layer_sink = layers.get(link.sink)
        if layer_src and layer_sink:
            layer_src = layer_src.get(link.layer)
            layer_sink = layer_sink.get(link.layer)
            if layer_src and layer_sink:
                if link.secure:

                    edge = Edge(color="darkgreen",
                                label=('<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD>'
                                       '<IMG SRC="icons/secure.png"/>'
                                       '</TD></TR></TABLE>>'))  # label='Secure'
                else:
                    edge = Edge(color="firebrick")
                layer_src >> edge << layer_sink

    def create_layer(self, layer, layer_name, nb_cmp):
        layer_style = self.layer_style.copy()
        if 'Business' in layer_name:
            layer_style['bgcolor'] = '#FAC1BD'
        elif not layer:
            layer_style['bgcolor'] = 'white'
        if layer:
            with Cluster(layer_name, graph_attr=layer_style):
                width = len(layer.components) / len(layer)
                cmp_name = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
                if width == 1:  # EndPOint : stack of components
                    cmp_label = ['<TR>', '</TR>']
                else:
                    cmp_label = ['', '']
                    cmp_name = f'{cmp_name} <TR>'
                for component in layer.components:
                    cmp_name = (f'{cmp_name}{cmp_label[0]}<TD PORT="{component.id_}">'
                                f'{component.id_} </TD>{cmp_label[1]}')
                if width != 1:
                    cmp_name = f'{cmp_name}</TR>'
                cmp_name = f'{cmp_name}</TABLE>>'
                return Diagramlayer(label=cmp_name, height=nb_cmp)

        with Cluster(layer_name, graph_attr=layer_style):
            return  Diagramlayer(label='')
