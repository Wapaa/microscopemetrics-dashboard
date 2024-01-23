from typing import Protocol


class DataSource(Protocol):
    def get_microscopes(self):
        pass

    def get_analysis_types(self, microscope):
        pass

    def get_analysis(self, microscope, analysis_type):
        pass

    def get_analysis_datasets(self):
        pass

    def get_analysis_dataset(self, analysis):
        pass
