#Copyright STACKEO - INRIA 2020 .
from distutils import util
import os
import xml.etree.ElementTree as ET

from jinja2 import Environment, Template
from Stkml.Drawio.Link import Link
from Stkml.Drawio.Node import Node
from Stkml.Drawio.Tier import Tier
from Stkml.Stkml import Stkml


class DrawIO:

    def __init__(self, default_icons: str, icons: str):
        self.default_icons = default_icons
        self._icon_dir = os.path.join(os.getcwd(), icons)
        self.tiers = []
        self.links = []
        self.layers = {'ServicelayerElement': 0,
                       'DatalayerElement': 0,
                       'MessaginglayerElement': 0,
                       'ConnectivitylayerElement': 0,
                       'NetworklayerElement': 0,
                       'PhysicallayerElement': 0,
                       'EnergylayerElement': 0}

        self.funcs = {1: self.creat_diagram_level1, 2: self.creat_diagram_level2}

    def add_tier(self, name, type_=None) -> Tier:
        tier = Tier(name, type_)
        if len(self.tiers) > 0:
            tier.position[0] = tier.position[0] + self.tiers[-1].position[0] + self.tiers[-1].dimension[0] + 30
        self.tiers.append(tier)
        return tier

    def add_link(self, node_source, node_sink, layer=None) -> None:
        self.links.append(Link(node_source, node_sink, layer))

    def get_node(self, node_: str) -> Node:
        nod = None
        for tier in self.tiers:
            for node in tier.nodes:
                if node_ in (node.ids[0], node.name):
                    nod = node
                    break
            else:
                continue
            break
        return nod

    def generate_drawio_xml(self, template: Template, output: str):
        xml = template.render(DrawIO=self)
        with open(f'{output}.drawio', 'w+') as drawio_file:
            drawio_file.write(xml)

    def generate_drawio_diagram(self, level: int, env: Environment, output: str):
        bound = self.funcs[level].__get__(
            self, type(self))
        return bound(env, output)


    def creat_diagram_level1(self, env: Environment, output: str):
        warnings = []
        for tier in self.tiers:
            for node in tier.nodes:
                node.generate_icon_uri()
                node.dimension = [70, 80]
            tier.generate_nodes_position_level1()
        self.center_tiers()
        sources = []
        sinks = []
        for link in self.links:
            if link.source.name not in sources or link.sink not in sinks and \
                link.layer == 'NetworklayerElement':# to not duplicate links
                sources.append(link.source.name)
                sinks.append(link.sink.name)
                link.source = link.source.ids[0]
                link.sink = link.sink.ids[0]
            else:
                link.display = False

        template = env.get_template('drawio/drawio.j2')
        self.generate_drawio_xml(output=output, template=template)
        return warnings

    def creat_diagram_level2(self, env: Environment, output: str):

        warnings = self.create_link_level2()
        for tier in self.tiers:
            for node in tier.nodes:
                hachting = True
                blank_layers = []
                for layer in node.layers[-1::-1]:
                    layer.update_height(self.layers[layer.type + 'layerElement'])
                    layer_len = layer.__len__()
                    if layer_len > 0:
                        hachting = False
                        blank_layers.clear()
                    elif layer_len == 0:
                        if hachting:
                            layer.hachting()
                        else:
                            blank_layers.append(layer)
                for layer in blank_layers:
                    layer.set_blank()

                node.generate_layers_position()
                node.set_dimensions()
            tier.generate_nodes_position_level2()



        self.center_tiers()
        template = env.get_template('drawio/drawio-layer.j2')
        self.generate_drawio_xml(output=output, template=template)
        return warnings

    def create_link_level2(self):
        sources = []
        sinks = []
        to_remove = []
        warnings = []
        for link in self.links:
            layer = link.layer
            if layer:
                src = link.source
                sink = link.sink
                if link.internal and src not in sources and sink not in sinks:
                    sources.append(src)
                    sinks.append(sink)
                    sink.un_stack()
                src = src.get_layer(layer)
                sink = sink.get_layer(layer)
                if src and sink:
                    link.source = src.ids[0]
                    link.sink = sink.ids[0]
                else:
                    to_remove.append(link)
                    if not src:
                        warnings.append(f'link source {link.source.name} does not have {layer} layer')
                    if not sink:
                        warnings.append(f'link sink {link.sink.name} does not have {layer} layer')
            else:
                to_remove.append(link)
                warnings.append(f'You did not specify the layer type on link between'
                                f'{link.source.name} ans {link.sink.name}')

        for i in to_remove:
            self.links.remove(i)
        return warnings

    def from_stkml(self, stkml: Stkml) -> str or None:
        for tier in stkml.tiers:
            drawio_tier = self.add_tier(name=tier.name, type_=tier.type)
            for node in tier.nodes:
                drawio_node = drawio_tier.add_node(name=node.id_, nature=node.nature, icon=node.icon)
                drawio_node.dimension = [210, 585]
                for layer_ in self.layers:
                    drawio_layer = drawio_node.add_layer(layer_.replace('layerElement', ''))
                    layer = node.get_layer_element(layer_)
                    if layer:
                        drawio_layer.hub = layer.hub and len(layer.components) > 1
                        for component in layer.components:
                            drawio_layer.add_component(name=component.id_, type_=component.component_type)
                    self.layers[layer_] = max(self.layers[layer_], drawio_layer.dimension[1])
        for link in stkml.links:
            source = self.get_node(link.source)
            sink = self.get_node(link.sink)
            if not source:
                return f'link source {link.source}  not found'
            if not sink:
                return f'link sink {link.sink}  not found'

            layer = link.layer
            self.add_link(source, sink, layer)
        return None

    def create_drawio(self, file) -> None:
        root = ET.parse(file).getroot()
        ids = {}
        for obj in root.iter('object'):
            if obj.get('Type') == 'Tier':
                tier, tier_id = self.create_tier(obj, root)
                #root.remove(obj)
                nodes = self.get_childs(root, ['Tier', tier_id], 'Node')
                for node in nodes:
                    node, node_id, ids = self.create_node(ids, node, tier)
                    #root.remove(Node)
                    layers = self.get_childs(root, [True, node_id], tag='mxCell')
                    for layer in layers:
                        ids = self.create_layer(ids, layer, node, root)

        for link in root.iter('mxCell'):
            self.create_link(ids, link, root)

    def create_link(self, ids: dict, link: ET, root: ET) -> None:
        if link.get('Type') == 'Link':
            layer_ = self.get_parent(root, link.get('source'))
            type_ = layer_.get('Type')
            if 'layerElement' in type_:
                layer_ = type_.replace('layerElement', '')
            else:
                layer_ = None
            self.add_link(ids[link.get('source')], ids[link.get('target')], layer=layer_)

    def create_layer(self, ids: dict, layer: ET, node: Node, root: ET) -> dict:
        layer = self.get_childs(root, [True, layer.get('id')], 'Layer')
        if layer:
            layer = layer[0]
            layer_id = layer.get('id')
            ids[layer_id] = node.name
            hub = bool(util.strtobool(layer.get('Hub')))
            layer_ = node.add_layer(layer.get('Type'), hub)
            layer_id = layer.find('mxCell').get('parent')
            if hub:
                layer_id = self.get_childs(root, [True, layer_id], child_type="Hub")[0].get('id')
            componenets = self.get_childs(root, [True, layer_id], child_type='Component')
            for componenet in componenets:
                name = componenet.get('label')
                for obj in root.iter('mxCell'):
                    component_id = obj.get('parent')
                    if component_id == componenet.get('id'):
                        name_ = obj.get('value')
                        if name_ != "" and name_ not in "<span>&lt;/&gt;</span>":
                            name = name_
                            break
                layer_.add_component(name, componenet.get('Type'))
        return ids

    def create_node(self, ids: dict, node: ET, tier: Tier):
        node_label = node.get('label')
        node_id = node.get('id')
        ids[node_id] = node_label
        node = tier.add_node(name=node_label, type_=node.get('Type'), nature='Hardware') # to do change uri to path
        return node, node_id, ids

    def create_tier(self, obj, root):
        tier = self.add_tier(obj.get('label'))
        tier_id = obj.find('mxCell').get('parent')
        tier_id = self.get_childs(root, [False, tier_id], 'label')
        tier_id = tier_id[0].find('mxCell').get('parent')
        return tier, tier_id

    def get_childs(self, root, parent, child_type=None, tag='object'): # parent = [parent_type, parent_id]
        childs = []
        for obj in root.iter(tag):
            if child_type:
                type_ = obj.get('Type')
                if type_ and child_type in type_:
                    if parent[0]:
                        if obj.find('mxCell').get('parent') == parent[1]:
                            childs.append(obj)
                    else:
                        if obj.get('id') == parent[1]:
                            childs.append(obj)
            else:
                if parent[0]:
                    if obj.get('parent') == parent[1]:
                        childs.append(obj)
                else:
                    if obj.get('id') == parent[1]:
                        childs.append(obj)
        return childs

    def get_parent(self, root: ET, children: ET, type_='object') -> ET or None:
        parent = None
        for parent in root.iter(type_):
            if parent.get('id') == children:
                break
        return parent


    def center_tiers(self) -> None :
        min_ = 0
        width = 0
        for tier in self.tiers:
            diff = tier.position[0] - width
            if diff < 0:
                tier.position[0] += abs(diff) + 30
            width = tier.position[0] + tier.dimension[0]
            min_ = min(min_, tier.dimension[1])

        for tier in self.tiers:
            tier.position[1] -= (tier.dimension[1] - min_)/2
