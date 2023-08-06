#Copyright STACKEO - INRIA 2020
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='stkml',
    version=get_version("Stkml/__init__.py"),
    packages=find_packages(exclude=["Stkml_tests"]),
    license='GNU Affero General Public License v3',
    author="Fraoui Zakaria",
    author_email="zakaria@stackeo.io",
    description="stkml is a transpiler for stckml language to generate output for different backend as diagram, drawio, map.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://stkml.stackeo.io/",
    entry_points={
        'console_scripts': [
            'stkml = Stkml.Cli:cli',
        ],
    },
    install_requires=[
        'click',
        'decorator',
        'diagrams',
        'folium',
        'geopy',
        'Jinja2',
        'jsonschema',
        'Pillow',
        'pyyaml',
        'prettytable'
    ],
    extras_require={
        'dev': [
            'pylint',
            'coverage',
            'tox',
            'twine'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Console"
    ],
    include_package_data=True,
    package_data={
        'templates': ['Stackml/templates/*'],
    },

)
