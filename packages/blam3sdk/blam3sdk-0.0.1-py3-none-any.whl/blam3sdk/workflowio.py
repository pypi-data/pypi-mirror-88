from abc import ABC
from typing import List

class WorkFlowIOData(ABC):
    def __init__(self):
        pass

class AssetsIO(WorkFlowIOData):
    def __init__(self, asset_ids: List[int]=[], is_empty=False):
        self.asset_ids = asset_ids
        return

class AssetVersionsIO(WorkFlowIOData):
    def __init__(self, asset_version_ids: List[int]=[], is_empty=False):
        self.asset_version_ids = asset_version_ids
        return

class AssetFilesIO(WorkFlowIOData):
    def __init__(self, asset_file_ids: List[int]=[], is_empty=False):
        self.asset_file_ids = asset_file_ids
        return

class FileStoresIO(WorkFlowIOData):
    def __init__(self, file_store_ids: List[int]=[], is_empty=False):
        self.file_store_ids = file_store_ids
        return

class NoneIO(WorkFlowIOData):
    def __init__(self):
        pass

class TextListIO(WorkFlowIOData):
    def __init__(self, text_list: List[str]=[], is_empty=False):
        self.text_list = text_list
        return

class WorkOrdersIO(WorkFlowIOData):
    def __init__(self, work_order_ids: List[int]=[], is_empty=False):
        self.work_work_ids = work_order_ids
        return
