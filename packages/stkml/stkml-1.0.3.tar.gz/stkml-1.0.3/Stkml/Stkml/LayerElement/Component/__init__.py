#Copyright STACKEO - INRIA 2020 .
class Component:

    def __init__(self, id_: str, type_: str):
        self.id_ = id_
        self.component_type = type_
        self.provider = None
        self.name = None
        self.role = None

    def set_name(self, name: str) -> None:
        self.name = name

    def set_role(self, role: str) -> None:
        self.role = role

    def set_provider(self, provider: str) -> None:
        self.provider = provider
