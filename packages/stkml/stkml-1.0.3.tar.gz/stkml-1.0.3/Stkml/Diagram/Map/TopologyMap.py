#Copyright STACKEO - INRIA 2020 .

from folium import folium, PolyLine, Map
from folium.plugins import MarkerCluster
from geopy import Nominatim

from Stkml.Diagram.Graphviz.RegionDiagram import RegionDiagram
from Stkml.Diagram.Map import RegionsMap
from Stkml.Diagram.Map.NodeMarker import NodeMarker
from Stkml.Diagram.Map.RegionNotFound import RegionNotFound
from Stkml.Stkml import Stkml


class TopologyMap(RegionsMap):

    def __init__(self, diagram_attr):
        self.style = diagram_attr #not used
        super().__init__()

    def from_stackml(self, stackml: Stkml, output: str) -> None:
        nodes = {}
        geolocator = Nominatim(user_agent="shttps://nominatim.openstreetmap.org/search/")
        topology_map = Map()  # tiles='Stamen Toner'Terrain
        marker_cluster = MarkerCluster(icon_create_function='''
                    function(cluster) {
                        var markers = cluster.getAllChildMarkers();
                        var sum = 0;
                        for (var i = 0; i < markers.length; i++) {
                            sum += markers[i].options.props.quantity;
                        }
                        return L.divIcon({
                             html: '<div style="color:#FFFFFF;text-align: center;vertical-align: middle;background-color:#006DC9;border-radius: 50% 50% 50% 50%;" <b>'+ sum + '</b></div>',
                             className: '{marker-cluster marker-cluster-small}',
                             iconSize: new L.Point(50, 50)

                        });
                    }
                ''').add_to(topology_map)
        map_bound = [[0, 0], [0, 0]]
        for region in stackml.regions:
            nodes[region.name] = {}
            location = geolocator.geocode(region.name)
            if not location:
                raise RegionNotFound(region)
            map_bound = self.get_map_bound(location, map_bound)
            lat_ = location.latitude
            long_ = location.longitude
            for node in region.nodes.items():
                nodes[region.name][node[0]] = [lat_, long_]
                _icon = stackml.get_node(node[0]).icon
                NodeMarker([lat_, long_], icon=_icon, node=node).add_to(marker_cluster)
                lat_ += 0.1
                long_ += 0.1
        for link in self.create_regions_links(nodes, stackml.links):
            topology_map.add_child(link)
        folium.FitBounds(bounds=map_bound, padding=[10, 10]).add_to(topology_map)
        topology_map.save(f'{output}.html')

    def get_map_bound(self, location, map_bound):
        if abs(location.latitude) > abs(map_bound[0][0]):
            map_bound[0] = [location.latitude, location.longitude]
        if abs(location.longitude) > abs(map_bound[-1][-1]):
            map_bound[1] = [location.latitude, location.longitude]
        return map_bound

    def create_regions_links(self, nodes, links):
        linked = []
        lines = []
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
                        lines.append(PolyLine(locations=[node_source, node_sink], color='blue'))

        # links between regions
        for link in links:
            if link.source not in linked:
                linked.append(link.source)
                nodes_source = RegionDiagram.get_all_nodes(nodes, link.source)
                nodes_sink = RegionDiagram.get_all_nodes(nodes, link.sink)
                for n_src in nodes_source:
                    for n_sink in nodes_sink:
                        lines.append(PolyLine(locations=[n_src, n_sink], color='blue'))

        return lines
