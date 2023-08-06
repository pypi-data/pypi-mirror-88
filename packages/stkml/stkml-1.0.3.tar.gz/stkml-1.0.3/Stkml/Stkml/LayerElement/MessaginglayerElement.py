#Copyright STACKEO - INRIA 2020 .
from Stkml.Stkml.LayerElement import LayerElement
from Stkml.Stkml.LayerElement.Component.MessagingComponent import MessagingComponent


class MessaginglayerElement(LayerElement):

    def __init__(self, name: str, hub):
        super().__init__(name, type(self).__name__, hub)

    def set_components(self, components) -> None:
        for component in components:
            messaging_component = MessagingComponent(id_=component.get('ComponentId'), c_type=component.get('nature'))
            protocol = component.get('protocol')
            if protocol is not None: #protocol != None
                messaging_component.set_protocol(protocol.get('name') + protocol.get('version'))
            for msg in (component.get('msg') or []):
                msg_ = messaging_component.add_message(type_=msg.get('type'), topic=msg.get('topicName'),
                                                       size=msg.get('sizeUnit'))
                msg_.set_action(msg.get('action'))
            self.add_component(messaging_component)
