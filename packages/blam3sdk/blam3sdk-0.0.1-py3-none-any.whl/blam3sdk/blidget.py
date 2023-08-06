import asyncio
import base64
import json
import os
import sys
import traceback

from abc import ABC, abstractmethod

from blam3sdk import blam
from blam3sdk.blam.extensions import deserialise, serialise
from blam3sdk.blidgetoutput import BlidgetOutput
from blam3sdk.runconfig import RunConfig
from blam3sdk.tokengenerator import TokenGenerator

class Blidget(ABC):
    def __init__(self, t_input, t_output) -> None:
        self.input_data_json = ""
        self.workflow_run_id = 0
        self._input_type = t_input
        self._output_type = t_output
        self._args = sys.argv

    async def execute_async(self):
        try:
            Blidget._send_running_message()

            self.run_config = self._load_debug_config() if (sys.gettrace() is not None) else self._load_config()
            self.input_data_json = json.dumps(self.run_config.input_data.__dict__)
            self.workflow_run_id = self.run_config.workflow_run_id

            self.init()
            await self.init_async()
            
            if not self.run_config.complete_only:
                output = await self.run_async(self.run_config.input_data)
            else:
                output = await self.complete_async(self.run_config.input_data)

            Blidget._send_success_Message(output)

        except Exception as err:
            Blidget._send_error_message(str(err), traceback.format_exc())

    def init(self):
        pass

    async def init_async(self):
        return asyncio.create_task(self._do_nothing())

    @abstractmethod
    async def run_async(self, input_data):
        pass

    async def complete_async(self, input_data):
        pass

    def return_true(self, output_data) -> None:
        self.return_complete(output_data)

    def return_false(self, output_data) -> None:
        self.return_complete(None, output_data)

    def return_complete(self, output_data_1, output_data_2=None) -> BlidgetOutput:
        return BlidgetOutput(is_complete=True,
                             primary_workflow_data=output_data_1,
                             secondary_workflow_data=output_data_2)

    def return_idle(self, run_state) -> BlidgetOutput:
        return BlidgetOutput(is_complete=False,
                             polling_interval_seconds=-1,
                             state=run_state)

    def return_waiting(self, run_state, polling_interval: int) -> BlidgetOutput:
        return BlidgetOutput(is_complete=False,
                             polling_interval_seconds=polling_interval,
                             state=run_state)

    def update_progress(self, perc: int=0, message: str="") -> None:
        Blidget._send_message({ "Type": "Progress", "ProgressPercentrage": perc, "Message": message })

    def get_argument(self, name: str):
        if name in self.arguments.keys():
            return self.arguments[name]
        return None

    def get_runstate(self, run_state_type):
        return run_state_type(**deserialise(self.run_state))

    async def _do_nothing(self):
        pass

    def _load_config(self) -> RunConfig:
        input_data_json = sys.stdin.readline()
        run_state_json = sys.stdin.readline()
        if run_state_json is None or run_state_json.strip() == "":
            run_state_json = "{}"

        return RunConfig(api_endpoint=self._args[1],
                         bearer_token=self._args[2],
                         arguments=json.loads(base64.decodebytes(self._args[3].encode('utf-8')).decode('utf-8')),
                         workflow_run_id=int(self._args[4]),
                         complete_only="-check" in self._args,
                         input_data=self._input_type(**deserialise(json.loads(input_data_json))),
                         run_state=json.loads(run_state_json))

    def _load_debug_config(self):
        with open(os.path.join(os.getcwd(),'debug.json'), 'r') as f:
            debugConfig = json.load(f)
        
        token_generator = TokenGenerator(debugConfig['tokenKey'])
        
        return RunConfig(api_endpoint=debugConfig['apiEndpoint'],
                         bearer_token=token_generator.generateToken(debugConfig['organisationId']),
                         arguments=debugConfig['arguments'],
                         workflow_run_id=0,
                         complete_only=debugConfig['completeOnly'],
                         input_data=self._input_type(**deserialise(debugConfig['inputData'])),
                         run_state=debugConfig['runState'])

    @staticmethod
    def _send_running_message():
        Blidget._send_message({ "Type": "Running" })
    
    @staticmethod
    def _send_success_Message(output_obj: BlidgetOutput):
        Blidget._send_message({ "Type": "Success", "OutputData": serialise(output_obj) })

    @staticmethod
    def _send_error_message(message: str, exception: str):
        Blidget._send_message({ "Type": "Error", "Message": message, "Exception": exception })

    @staticmethod
    def _send_message(message_obj):
        serialised_json = json.dumps(message_obj)
        print(serialised_json)

    @staticmethod
    def _write_to_file(text, filename):
        with open(filename,'at',encoding='utf-8') as fopen:
            fopen.write(text)
