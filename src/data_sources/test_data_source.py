## This data source is providing mocked data to the tests.
from typing import Dict, List

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
from linkml_runtime.utils.schemaview import SchemaView


class DataSource:
    def __init__(self, service, login, password):
        self.connection = None
        self.schema_view = SchemaView(mm_schema.microscopemetrics_schema)

    def get_user(self):
        return "Here is the user"

    def get_microscopes(self) -> Dict[str, mm_schema.Microscope]:
        return {
            "microscope1": mm_schema.Microscope(
                id="microscope1",
                name="microscope1",
                description="A microscope",
                manufacturer="Manufacturer1",
                serial_number="SerialNumber1",
                model="Model1",
                type="WIDE-FIELD",
                url="https://example.com/microscope1",
            ),
            "microscope2": mm_schema.Microscope(
                id="microscope2",
                name="microscope2",
                description="A microscope",
                manufacturer="Manufacturer2",
                serial_number="SerialNumber1",
                model="Model2",
                type="WIDE-FIELD",
                url="https://example.com/microscope2",
            ),
        }

    def get_analysis_types(self, microscope: mm_schema.Microscope) -> List[mm_schema.AnalysisType]:
        return self.schema_view.class_children("MetricsDataset")

    def get_analysis(
        self, microscope: mm_schema.Microscope, analysis_type: mm_schema.AnalysisType
    ) -> Dict[str, mm_schema.Analysis]:
        return {
            "analysis1": mm_schema.Analysis(
                name="analysis1",
                description="An analysis",
                url="https://example.com/analysis1",
            ),
            "analysis2": mm_schema.Analysis(
                name="analysis2",
                description="An analysis",
                url="https://example.com/analysis2",
            ),
        }

    def get_analysis_datasets(
        self,
    ):
        pass

    def get_analysis_dataset(self, analysis: mm_schema.MetricsDataset) -> mm_schema.MetricsDataset:
        pass

    def get_image_data(self, image: mm_schema.Image) -> np.ndarray:
        pass
