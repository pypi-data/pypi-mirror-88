#Copyright STACKEO - INRIA 2020
#!/usr/bin/python
import os
MODULE_DIR = os.path.realpath(os.path.join(__file__, '..'))
STKML_URL_SCHEMA = 'https://stkml.stackeo.io/_static/stackml.schema.json'
STKML_PACKAGES = '.stkml_packages'
STKML_EXTENSION = '.stkml.yaml'
ICONS = os.path.join(MODULE_DIR, 'templates/diagram/resources/')
__version__ = '1.0.3'
STACKIHUB_URL = 'http://localhost/api/v1/'
STKML_METADATA = os.path.join(MODULE_DIR, 'templates', 'StkmlIn', 'stkml.yaml.json')
