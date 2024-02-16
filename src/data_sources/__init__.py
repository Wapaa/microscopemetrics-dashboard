from typing import Dict, List, Protocol

import microscopemetrics_schema.datamodel as mm_schema


class DataSource(Protocol):
    def __init__(self, service, login, password):
        self.connection = (service, login, password)

    def get_user(self, connection):
        raise NotImplementedError

    def get_microscopes(self, connection) -> Dict[str, mm_schema.Microscope]:
        raise NotImplementedError

    def get_analysis_types(
        self, connection, microscope: mm_schema.Microscope
    ) -> Dict[mm_schema.MetricsDataset.name, mm_schema.AnalysisType]:  # TODO: how?
        raise NotImplementedError

    def get_analysis_dataset_uris(
        self, connection, microscope: mm_schema.Microscope, analysis_type: mm_schema.AnalysisType
    ) -> Dict[mm_schema.MetricsDataset.name, mm_schema.MetricsDataset.dataset_uri]:
        raise NotImplementedError

    def get_analysis_dataset(
        self, connection, dataset_uri: mm_schema.MetricsDataset.dataset_uri
    ) -> mm_schema.MetricsDataset:
        raise NotImplementedError

    def get_image(self, image_uri: mm_schema.Image.image_url) -> mm_schema.Image5D:
        raise NotImplementedError

    def get_key_value_pairs(self, connection, source_object: mm_schema.uri) -> mm_schema.KeyValues:
        raise NotImplementedError
