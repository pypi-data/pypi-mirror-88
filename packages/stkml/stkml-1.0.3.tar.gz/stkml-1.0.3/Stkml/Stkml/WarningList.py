#Copyright STACKEO - INRIA 2020 .
from typing import List

class WarningList(Exception):

    def __init__(self, warnings: List[str]):
        super().__init__()
        self.warnings = warnings

    def __str__(self):
        warnings = ''
        for warn in self.warnings:
            warnings = f'{warnings}{warn}\n'
        return warnings
