import os
import time
import json
from datetime import datetime
from types import MappingProxyType
from copy import deepcopy

from sopic.utils.dag import is_valid_dag, graph_to_dot
from sopic.utils.settings import overwrite_settings_values, step_settings


class Station:
    STATION_NAME = ""
    STATION_ID = 0
    STATION_VERSION = None

    dag = []
    start_step_key = None

    _run_info = {}

    # ---

    # path to settings file
    default_settings_dir = "~/.sopic/settings/"

    # default settings that will be overwritten by the values from the settings
    # file
    default_settings = {}

    # settings of the station
    _settings = {}

    # Optional password for the settings dialog
    admin_password = None

    def __init__(self, next_step_handlerUI, end_run_handlerUI):
        if self.start_step_key is None:
            # TODO: add warning log
            self.start_step_key = list(self.dag.keys())[0]

        self._next_step_handlerUI = next_step_handlerUI
        self._end_run_handlerUI = end_run_handlerUI

        self._validate_dag()
        self._init_steps()
        self._load_settings()
        self._init_run_info()

    # ensure the `self.dag` variable is a valid DAG
    def _validate_dag(self):
        if not is_valid_dag(self.dag):
            raise Exception("self.dag should be a valid directed acyclic graph")

        # TODO: use a better switch to print the dot file
        if self.DEBUG:
            graph_to_dot(self.dag, self.start_step_key, self.STATION_NAME)

    # init each step class with proper parameters
    def _init_steps(self):
        for key, (step, childs) in self.dag.items():
            self.dag[key] = (
                step(childs, None),  # self.logger,
                childs,
            )

    def _get_settings_file_path(self):
        return os.path.join(
            os.path.expanduser(self.default_settings_dir),
            self.STATION_NAME + ".json",
        )

    # load the settings from the json file
    def _load_settings(self):
        if self.default_settings is not None:
            self._settings = deepcopy(self.default_settings)

        try:
            with open(self._get_settings_file_path()) as data:
                self._settings = overwrite_settings_values(
                    self._settings,
                    json.load(data),
                )
        except Exception:
            # TODO add error logging
            return

    # handler to return the settings, used by the settigns dialog
    def _get_settings_handler(self):
        return deepcopy(self._settings)

    # handler to reset the settings to the default values defined in the
    # station file
    def _reset_settings_handler(self):
        try:
            os.remove(self._get_settings_file_path())
        except OSError:
            # TODO logger
            pass
        self._load_settings()

    # handler to save the new settings
    def _save_settings_handler(self, settings):
        settings_path = self._get_settings_file_path()
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)

        self._settings = settings

        with open(settings_path, "w") as file:
            json.dump(self._settings, file)

    def _init_run_info(self):
        self._run_info = self._get_empty_run_info()

    def _get_empty_run_info(self):
        return {
            "info": {
                "id": self.STATION_ID,
                "name": self.STATION_NAME,
            },
            "errors": [],
            "run": {
                "success": True,
                "consecutive_failed": 0,
                "nb_failed": 0,
                "nb_run": 0,
                "last_failed_step": None,
                "start_date": None,
            },
        }

    def _reset_run_info(self):
        run_info = {
            **(self._get_empty_run_info()),
            "run": {
                **self._run_info["run"],
            },
        }
        run_info["run"]["last_failed_step"] = None
        return run_info

    def start(self):
        while True:
            self._run_info = self._reset_run_info()
            print('----- start run')
            self.start_run_handler()
            is_success = self._run()
            self.end_run_handler(is_success)
            print('----- end run')

    def start_run_handler(self):
        self._run_info["run"]["start_date"] = datetime.utcnow()
        # TODO: logging

    def _run(self):
        is_success_run = True
        step_key = self.start_step_key

        context = dict()
        number_retries = 0

        # while the current step has child, we continue the run
        while step_key in self.dag.keys():
            print(f'[{step_key}]')
            (step, childs) = self.dag[step_key]

            self._next_step_handlerUI(step)

            try:
                # TODO
                # Run the step
                step_result = step.start(
                    context,
                    # we could find a way to return an immutable object instead
                    # of performing a copy. The immutability needs to be run
                    # recursively on the value
                    deepcopy(step_settings(self._settings)),
                    MappingProxyType(self._run_info)
                )
            except Exception as e:
                print('step uncatch error:')
                print(e)
                print('step.childs: ', step._childs)
                step_result = step.buildStepResult(
                    False,
                    next_step_key=step.get_step_key('_err'),
                    infoStr=str(e),
                    errorCode=-1,
                )
                # TODO: custom `step_result`
                # Catch any non-catched exception with a default errorCode

            print('step_result: ', step_result)
            next_step_key = step_result["nextStepKey"]

            if len(childs) != 0:
                if next_step_key is None:
                    # raise error if the next step is not defined and multiple
                    # steps are possible
                    if len(childs) != 1:
                        raise Exception(f"Multiple potential next steps for step {step_key}")
                    # otherwise take the step defined in self.dag
                    if type(childs) is dict:
                        # if it's a dict, we first need to convert to a list
                        next_step_key = list(childs.values())[0]
                    else:
                        next_step_key = childs[0]
                # raise exception if the next step is not defined as a potential
                # step in self.dag
                if next_step_key not in self.dag.keys():
                    raise Exception(f"Step {next_step_key} is not a child of step {step_key}")

            print('next_step_key: ', next_step_key)

            # The step has passed
            if step_result["isSuccess"]:
                # TODO: logging
                step.end()
                number_retries = 0
                step_key = next_step_key
                continue

            # The step has failed

            # If the step has not reach its max number of retries,
            # we will relaunch the same step on the next loop iteration
            if step.MAX_RETRIES != 0 and number_retries < step.MAX_RETRIES:
                # TODO: logging
                number_retries += 1
                next_step_key = step_key
                step.end()
                # give a little bit of time before restarting the same step
                # we could use an incremental timer, or remove it completly
                time.sleep(0.5)
                continue

            # The max number of retries is reached, or the step has no retry
            is_success_run = False
            number_retries = 0

            # Track the name of the last step that has failed
            # Can be used to track the run status
            self._run_info["run"]["last_failed_step"] = step.STEP_NAME
            # When an errorCode is available, store it in the errors array
            if step_result["errorCode"] is not None:
                self._run_info["errors"].append(
                    {
                        "step": step.STEP_NAME,
                        "errorCode": step_result["errorCode"],
                        "infoStr": step_result["infoStr"],
                    }
                )
            # TODO: logging
            step.end()
            step_key = next_step_key
        return is_success_run

    def end_run_handler(self, is_success):
        self._run_info["run"]["success"] = is_success
        self._run_info["run"]["consecutive_failed"] = (
            self._run_info["run"]["consecutive_failed"] + 1
            if not is_success else 0
        )
        self._run_info["run"]["nb_run"] += 1
        if not is_success:
            self._run_info["run"]["nb_failed"] += 1

        self._end_run_handlerUI(
            self._run_info["run"]["nb_failed"],
            self._run_info["run"]["nb_run"],
            self._run_info["run"]["start_date"],
            self._run_info["run"]["consecutive_failed"]
        )

        # TODO: logging

    def get_steps(self):
        return [i[0] for i in self.dag.values()]
