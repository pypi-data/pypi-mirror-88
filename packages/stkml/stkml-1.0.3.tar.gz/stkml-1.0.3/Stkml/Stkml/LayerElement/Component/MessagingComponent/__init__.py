#Copyright STACKEO - INRIA 2020 .
from typing import List

from Stkml.Stkml.LayerElement.Component import Component
from Stkml.Stkml.LayerElement.Component.MessagingComponent.Message import Message


class MessagingComponent(Component):

    def __init__(self, id_: str, c_type: str):
        super().__init__(id_=id_, type_=c_type)
        self.protocol = None
        self.msgs: List[Message] = []

    def set_protocol(self, protocol: str) -> None:
        self.protocol = protocol

    def add_message(self, type_: str, topic: str, size: str) -> Message:
        msg = Message(type_=type_, topic=topic, size=size)
        self.msgs.append(msg)
        return msg
