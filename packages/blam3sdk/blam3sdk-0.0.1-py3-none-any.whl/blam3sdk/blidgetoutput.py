from abc import ABC
from typing import Any

from blam3sdk.blam.extensions import serialise
from blam3sdk.workflowio import AssetFilesIO, AssetVersionsIO, AssetsIO, FileStoresIO, TextListIO, WorkOrdersIO

class BlidgetOutput(ABC):
    def __init__(self, is_complete:bool=False,
                       polling_interval_seconds:int=0,
                       state:Any=None,
                       primary_workflow_data:Any=None,
                       secondary_workflow_data:Any=None):
        self.is_complete = is_complete
        self.polling_interval_seconds = polling_interval_seconds
        self.state = serialise(state) if state is not None else None
        self.output_type = BlidgetOutput._get_output_type(primary_workflow_data) if primary_workflow_data is not None else BlidgetOutput._get_output_type(secondary_workflow_data)
        self.primary_workflow_data = serialise(primary_workflow_data) if primary_workflow_data is not None else None
        self.secondary_workflow_data = serialise(secondary_workflow_data) if secondary_workflow_data is not None else None

    @staticmethod
    def _get_output_type(output_obj) -> str:
        props = output_obj.__dict__.keys()
        if len(props) == 0:
            return "none"
        if len(props) == 1:
            if isinstance(output_obj, AssetsIO):
                return "assets"
            if isinstance(output_obj, AssetVersionsIO):
                return "assetVerions"
            if isinstance(output_obj, AssetFilesIO):
                return "assetFiles"
            if isinstance(output_obj, FileStoresIO):
                return "fileStores"
            if isinstance(output_obj, WorkOrdersIO):
                return "custom"
            if isinstance(output_obj, TextListIO):
                return "textList"
        return "custom"