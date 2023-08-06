#Copyright STACKEO - INRIA 2020 .
from typing import List

from Stkml.Stkml.LayerElement import LayerElement
from Stkml.Stkml.LayerElement.Component.DataComponent import DataComponent, Job


class DatalayerElement(LayerElement):

    def __init__(self, name: str, hub):
        super().__init__(name, type(self).__name__, hub)


    def set_components(self, components) -> None:
        for component in components:
            data_component = DataComponent(id_=component.get('name'), c_type=component.get('nature'))
            for job in (component.get('Workflow') or []):
                job_ = data_component.add_job(job.get('JobId'))
                for prec in (job.get('prec') or []):
                    job_.add_prec(prec)
                for arg in job.get('Args'):
                    arg_ = job_.add_arg(name=arg.get('name'), type_=arg.get('type'))
                    data = arg.get('data')
                    size = data.get('size')
                    arg_.add_data(size=size.get('value'), size_unit=size.get('unit'),
                                  type_=data.get('valueType'), reference=data.get('valueRef'))
            self.add_component(data_component)
