#Copyright STACKEO - INRIA 2020 .
from Stkml.Stkml.LayerElement import LayerElement
from Stkml.Stkml.LayerElement.Component.BusinessComponent import BusinessComponent


class BusinesslayerElement(LayerElement):

    def __init__(self, name: str, hub):
        super().__init__(name, type(self).__name__, hub)


    def set_components(self, components) -> None:
        for component in components:
            business_component = BusinessComponent(id_=component.get('name'), c_type=component.get('nature'),
                                                   type_=component.get('type'))
            business_component.set_value(value=component.get('value'))
            business_component.set_unit(unit=component.get('unit'))
            business_component.set_period(period=component.get('period'))
            self.add_component(business_component)
