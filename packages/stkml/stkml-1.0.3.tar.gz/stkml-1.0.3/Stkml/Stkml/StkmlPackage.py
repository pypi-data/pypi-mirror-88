#Copyright STACKEO - INRIA 2020 .
import json
import os

import yaml
from jinja2 import Environment
from jsonschema import validate

from Stkml import STKML_METADATA, STKML_PACKAGES


class StkmlPackage:

    def __init__(self, package: str):
        self.package_dir = package
        self.name: str = ''
        self.version: str = ''
        self.author: str = ''
        self.get_name_from_path()

    def get_name_from_path(self):
        self.name = os.path.basename(self.package_dir)

    def generate_package(self, environment: Environment) -> None:
        package_template = environment.get_template('StkmlIn/package.stkml.yaml.j2')
        package = package_template.render()
        package_file = os.path.join(self.package_dir, f'{self.name}.stkml.yaml')
        with open(package_file, 'w') as file:
            file.write(package)

    def generate_metadata(self, environment: Environment) -> None:
        metadata_template = environment.get_template('StkmlIn/stkml.yaml.j2')
        metadata = metadata_template.render(package=self)
        metadata_file = os.path.join(self.package_dir, 'stkml.yaml')
        with open(metadata_file, 'w') as file:
            file.write(metadata)

    @classmethod
    def check_metadata(cls, metadata_path):
        if not os.path.isfile(metadata_path):
            raise FileNotFoundError(f'can not find stkml metadata in {metadata_path}')
        with open(metadata_path, 'r') as meta_file:
            metadata = yaml.load(meta_file, Loader=yaml.FullLoader)
            with open(STKML_METADATA, 'r') as file:
                metadata_schema = json.load(file)
                validate(metadata, metadata_schema)
    @classmethod
    def get_packages_dir(cls, stkml_folder):
        stkml_folder = os.path.abspath(stkml_folder)
        packages_dir = os.path.join(stkml_folder, STKML_PACKAGES)
        if not os.path.isdir(packages_dir):
            stkml_folder = os.path.join(stkml_folder, os.pardir)
            try:
                return cls.get_packages_dir(stkml_folder)
            except RecursionError as error:
                raise RecursionError('can not find .stkml_packages folder ') from error
        return os.path.realpath(packages_dir)
