#Copyright STACKEO - INRIA 2020 .
from typing import List


import jsonschema
from jsonschema import Draft7Validator

import yaml
from yaml.composer import Composer
from yaml.constructor import Constructor

class StkmlSyntaxicError(Exception):

    def __init__(self, schema: dict, file: dict, file_name: str):
        super().__init__()
        self.schema = schema
        self.file = file
        self.file_name = file_name
        self.errors_list: List[jsonschema.exceptions.ValidationError] = []


    def get_all_errors(self):
        validator = Draft7Validator(self.schema)
        errors = sorted(validator.iter_errors(self.file), key=lambda e: e.path)

        not_error_list = []
        for error in errors:
            self.get_errors_list(error, not_error_list=not_error_list)


    def get_errors_list(self, error, not_error_list):
        if len(error.context) == 0 and error.instance not in not_error_list and error not in self.errors_list:
            self.errors_list.append(error)
            return
        not_error_list.append(error.instance)
        for er_ in error.context:
            self.get_errors_list(er_, not_error_list)


    def get_path(self, error: jsonschema.exceptions.ValidationError, yaml_line_nb: dict) -> (str, int):
        error = list(error.absolute_path)
        path = error[0]
        line = yaml_line_nb[path]
        for path_ in error[1:]:
            line_ = line[path_]
            if isinstance(line_, (list, dict)):
                line = line_
            if isinstance(path_, int):
                path += '[' + str(path_) + ']'
            else:
                path += '["' + path_ + '"]'
        if isinstance(line, list):
            line = line[0]
        return path, line['__line__']

    def __str__(self) -> str:
        self.get_all_errors()
        yaml_nb = self.create_yaml_with_line_number()
        msg = f'{len(self.errors_list)} error(s) in {self.file_name}\n'
        for error in self.errors_list:
            _, line = self.get_path(error, yaml_nb)# path
            msg += f'{error.message} in "{self.file_name}", line {line}\n' #on {path}
        return msg

    def create_yaml_with_line_number(self):
        loader = yaml.Loader(open(self.file_name).read())

        def compose_node(parent, index):
            # the line number where the previous token has ended (plus empty lines)
            line = loader.line
            node = Composer.compose_node(loader, parent, index)
            node.__line__ = line + 1
            return node

        def construct_mapping(node, deep=False):
            mapping = Constructor.construct_mapping(loader, node, deep=deep)
            mapping['__line__'] = node.__line__
            return mapping

        loader.compose_node = compose_node
        loader.construct_mapping = construct_mapping
        data = loader.get_single_data()
        return data
