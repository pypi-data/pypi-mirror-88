#Copyright STACKEO - INRIA 2020 .
from typing import List

from Stkml.Stkml import StkmlSyntaxicError


class StkmlSyntaxicErrorList(Exception):

    def __init__(self, errors: List[StkmlSyntaxicError]):
        super().__init__()
        self.errors = errors

    def __str__(self):
        errors_str = ''
        for error in self.errors:
            errors_str = f'{errors_str}{error.__str__()}'
        return errors_str
