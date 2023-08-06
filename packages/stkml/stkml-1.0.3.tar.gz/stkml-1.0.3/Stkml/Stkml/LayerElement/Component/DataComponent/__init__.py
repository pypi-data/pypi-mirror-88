#Copyright STACKEO - INRIA 2020 .
from typing import List

from Stkml.Stkml.LayerElement.Component import Component
from Stkml.Stkml.LayerElement.Component.DataComponent.Job import Job


class DataComponent(Component):

    def __init__(self, id_: str, c_type: str):
        super().__init__(id_=id_, type_=c_type)
        self.workflow: List[Job] = []


    def add_job(self, id_: str) -> Job:
        job = Job(id_)
        self.workflow.append(job)
        return job
