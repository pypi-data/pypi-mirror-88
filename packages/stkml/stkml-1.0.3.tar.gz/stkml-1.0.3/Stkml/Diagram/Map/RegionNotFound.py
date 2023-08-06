#Copyright STACKEO - INRIA 2020 .
from Stkml.Stkml import Region


class RegionNotFound(Exception):

    def __init__(self, region: Region):
        super().__init__()
        self.region = region


    def __str__(self):
        return f'{self.region.name} region does not found'
