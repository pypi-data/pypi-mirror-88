#Copyright STACKEO - INRIA 2020 .
class Message:

    def __init__(self, type_: str, topic: str, size: str):
        self.type = type_
        self.topic = topic
        self.size = size
        self.action = None # publish subscribe

    def set_action(self, action: str) -> None:
        self.action = action
