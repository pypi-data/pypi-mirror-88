#Copyright STACKEO - INRIA 2020 .

class ModelException(Exception):

    def __init__(self, file: str = None, node_id: str = None, msg: str = None):
        super().__init__()
        self.file = file
        self.node_id = node_id
        self.msg = msg

    def no_node_model(self):
        self.msg = f'There no NodeModels on {self.file}'

    def no_modeldef(self):
        self.msg = f'There no modeldef for {self.node_id}'

    def node_not_found(self):
        self.msg = f'The {self.node_id} model does not exist on {self.file} '

    def __str__(self):
        return self.msg
