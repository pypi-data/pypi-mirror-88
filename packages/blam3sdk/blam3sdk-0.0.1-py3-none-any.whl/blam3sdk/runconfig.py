from typing import Any

class RunConfig(object):
    def __init__(self, api_endpoint: str="",
                       bearer_token: str="",
                       arguments: Any={},
                       workflow_run_id: int=0,
                       complete_only: bool=False,
                       input_data: Any={},
                       run_state: Any={},
                       organisation_id: int=1):
        self.api_endpoint = api_endpoint
        self.bearer_token = bearer_token
        self.arguments = arguments
        self.workflow_run_id = workflow_run_id
        self.complete_only = complete_only
        self.input_data = input_data
        self.run_state = run_state
        self.organisation_id = organisation_id
        return