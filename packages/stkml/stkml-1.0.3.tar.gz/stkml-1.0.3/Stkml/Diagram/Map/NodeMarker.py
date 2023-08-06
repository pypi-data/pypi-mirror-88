#Copyright STACKEO - INRIA 2020 .


from PIL import Image
from folium import Marker, features, Popup
from jinja2 import Template

class NodeMarker(Marker):

    _template = Template(u"""
           {% macro script(this, kwargs) %}
           var {{this.get_name()}} = L.marker(
               [{{this.location[0]}}, {{this.location[1]}}],
               {
                   icon: new L.Icon.Default(),
                   {%- if this.draggable %}
                   draggable: true,
                   autoPan: true,
                   {%- endif %}
                   {%- if this.props %}
                   props : {{ this.props }}
                   {%- endif %}
                   }
               )
               .addTo({{this._parent.get_name()}});
           {% endmacro %}
           """)

    def __init__(self, location, icon, node):
        label = node[0]
        self.quantity = node[1]
        if self.quantity > 1:
            label = str(self.quantity)+'\n'+label
        size = Image.open(icon).size
        if size[0] < size[1]:
            width = size[1]*50/size[0]
            height = 50
        else:
            height = size[0] * 50 / size[1]
            width = 50
        self.icon = features.CustomIcon(icon_image=icon, icon_size=(height, width))
        super().__init__(location=location, icon=self.icon, popup=Popup(label))
        self.props = {'quantity': self.quantity}
