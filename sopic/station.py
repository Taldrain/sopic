import os
import json
import time

from .utils import getLogger

STEP_SKIPPED = 'skipped'
STEP_RETRY = 'retry'
STEP_OK = 'ok'
STEP_KO = 'ko'
RUN_TERMINATED = 'terminated'

# stepDef is the step from the step array defined in a station.py file.
# It can, sometimes, be a tuple (step, boolean) to overwrite the ACTIVATED
# flag of the step.
def initStep(stepDef, stationName, stationId, logger):
    if (isinstance(stepDef, tuple)):
        return stepDef[0](stationName, stationId, logger, stepDef[1] != False)

    return stepDef(stationName, stationId, logger, True)

#
# Station class
#
class Station:
    # list of steps that will not steps the current run
    # by default a failure end the run
    nonBlockingSteps = [""]

    # list of steps that should be skip if a previous step (a non blocking
    # step) has failed
    stepsSkippedOnPreviousFail = [""]

    # Id of the previous station, checked at the start of the run
    # None to disable the check
    previousStationId = None

    # StepsData available for all steps, and defined in the child stations
    # Used for data shared between multiple steps
    defaultStepsData = {}

    defaultSettings = {}
    settings = None

    # path to logs file, if enabled
    default_log_dir = "~/.sopic/logs/"

    # should the log to file be enabled
    disable_file_logging = False

    # disable all logger handlers
    disable_handlers = False

    # path to settings file
    default_settings_dir = "~/.sopic/settings/"

    # nextStepHandler: handler called when a new step start
    # clearStepsHandlerUI: handler called when starting a new run
    # stepOKHandler: handler called when a step is OK
    # stepKOHandler: handler called when a step is KO
    def __init__(
        self,
        nextStepHandlerUI = None,
        clearStepsHandlerUI = None,
        stepOKHandlerUI = None,
        stepKOHandlerUI = None,
        skipStepHandlerUI = None
    ):
        self.logger = getLogger(
            self.STATION_NAME,
            self.STATION_ID,
            self.disable_file_logging,
            self.default_log_dir,
            self.disable_handlers,
        )
        self.steps = list(map(lambda x: initStep(
            x,
            self.STATION_NAME,
            self.STATION_ID,
            self.logger,
        ), self.steps))
        self.stepIndex = 0

        self.nextStepHandlerUI = nextStepHandlerUI
        self.clearStepsHandlerUI = clearStepsHandlerUI
        self.stepOKHandlerUI = stepOKHandlerUI
        self.stepKOHandlerUI = stepKOHandlerUI
        self.skipStepHandlerUI = skipStepHandlerUI

        self.settingsPath = os.path.join(
            os.path.expanduser(self.default_settings_dir),
            self.STATION_NAME + '.json',
        )

        if (self.defaultSettings is not None):
            self._readSettingFile()

        self._initStepData({
            "success": True,
            "consecutive_failed": 0,
            "nb_failed": 0,
            "nb_run": 0,
        })

        self.logger.debug("Starting station")

    def _readSettingFile(self):
        self.settings = self.defaultSettings.copy()
        try:
            with open(self.settingsPath) as settingsRaw:
                settingsData = json.load(settingsRaw)
                self.settings.update(settingsData)
        except:
            return

    def _initStepData(self, previousRunInfo=None):
        self.stepsData = {
            **self.defaultStepsData,
            **{
                "__status": {
                    "id": self.STATION_ID,
                    "name": self.STATION_NAME,
                    "previousStationId": self.previousStationId,
                },
                "__settings": self.settings,
                "__errors": [],
                "__run": previousRunInfo,
            },
        }

    def updateValueSettings(self, key, value):
        self.settings[key] = value
        self.stepsData['__settings'] = self.settings

    # Dump the settings into a file
    def updateSettingsFile(self):
        os.makedirs(os.path.dirname(self.settingsPath), exist_ok=True)

        with open(self.settingsPath, 'w') as f:
            json.dump(self.settings, f)

    # Resets the settings of the station by removing the local file
    # and re-setting the settings variable
    def resetSettings(self):
        try:
            os.remove(self.settingsPath)
        except OSError:
            pass
        # TODO is self.settings used
        # we could just used __settings
        self.settings = self.defaultSettings.copy()
        self.stepsData['__settings'] = self.settings

    # Return the name of the station
    def getDisplayName(self):
        return self.DISPLAY_NAME

    # Return the list of Steps
    def getSteps(self):
        return self.steps

    # Return the current step
    def getCurrentStep(self):
        return self.stepIndex

    # Start the station
    def start(self):
        while True:
            self.stepIndex = 0
            self.clearStepsHandlerUI()
            isSuccessRun = self.run()
            self._initStepData({
                "success": isSuccessRun,
                "consecutive_failed": (
                    self.stepsData["__run"]["consecutive_failed"] + 1 if (not isSuccessRun) else 0),
                "nb_run": (self.stepsData["__run"]["nb_run"] + 1),
                "nb_failed": (self.stepsData["__run"]["nb_failed"] + 1 if (not isSuccessRun) else self.stepsData["__run"]["nb_failed"]),
            })
            self.logger.info("Ending run ---------------------------------------")

    # Start a run
    def run(self):
        self.logger.info("Starting run")

        number_retries = 0

        isSuccessRun = True

        # Iterate on all steps
        while self.stepIndex < len(self.steps):
            step = self.steps[self.stepIndex]

            self.nextStepHandlerUI()

            # Skip the step, it's been deactivated
            if (step.ACTIVATED == False):
                self.logger.warning("Skipping step {} - the step has been deactivated".format(step.STEP_NAME))
                self.endStepHandler(STEP_SKIPPED, step)
                continue

            # Skip the step, a previous step has failed and this step is tagged as skip on fail
            if (step.STEP_NAME in self.stepsSkippedOnPreviousFail and not isSuccessRun ):
                self.logger.error("Skipping step {} - a previous step has failed".format(step.STEP_NAME))
                self.endStepHandler(STEP_SKIPPED, step)
                continue

            try:
                # Run the step
                stepResult = step.start(self.stepsData)
            except Exception as e:
                # Catch any non-catched exception with a default errorCode
                # The run is also terminated
                stepResult = step.buildStepResult(False, True, e, 255)
                self.logger.error("Exception not catch in step {}: {}".format(step.STEP_NAME, e))

            # The step has passed
            if (stepResult["passed"]):
                # Save the stepData object
                self.stepsData[step.STEP_NAME] = stepResult["stepData"]
                self.endStepHandler(STEP_OK, step)
                # Reset the number of retries
                number_retries = 0
            else:
                # The step has failed

                # Track if the step has terminated
                if (stepResult["terminate"]):
                    self.stepsData["__status"]["terminated"] = True

                # If the step has not reach its max number of retries,
                # we will relaunch the same step on the next loop iteration
                if (stepResult["max_retries"] != 0 and number_retries < stepResult["max_retries"]):
                    number_retries += 1
                    self.logger.info("Retrying step")
                    self.endStepHandler(STEP_RETRY, step)
                    continue

                # The max number of retries is reached, or the step has no retry
                isSuccessRun = False
                number_retries = 0
                # Track the name of the last step that has failed
                # Can be used to track the run status
                self.stepsData["__status"]["lastFailedStep"] = step.STEP_NAME
                self.stepsData[step.STEP_NAME] = stepResult["stepData"]
                # When an errorCode is available, store it in the __errors array
                if (stepResult["errorCode"] is not None):
                    self.stepsData["__errors"].append((step.STEP_NAME, stepResult["errorCode"], stepResult["errorStr"]))


                # The step is non blocking, and the station is not in a terminate run
                if (self.isNonBlockingStep(step.STEP_NAME) and stepResult["terminate"] == False):
                    # The step has failed, but the station will start the next step
                    self.logger.debug("Non-Blocking step reached")
                    self.endStepHandler(STEP_KO, step)
                else:
                    # Blocking step, or terminate run, the station will go to the last step
                    self.logger.debug("Blocking step reached, go to last step")
                    self.endStepHandler(RUN_TERMINATED, step)

        return isSuccessRun



    # handler of end step
    #
    # TODO we could simplify by merging some statements
    # -> update ui (OK, KO, retry)
    # -> update the step (step.end())
    # -> update the index
    #   - we could also rework how the index is dealt, we could replace the
    #     `while` loop with a `for` loop and prevent any manual update of the
    #     index. This would be clearer and force use to go through all steps.
    #     We would just have to track a "terminated" run to skip the step.
    #     Having a end run step would also be cleaner, insted of having to run
    #     the last step, even in terminated run.
    def endStepHandler(self, status, step):
        if (status == STEP_SKIPPED):
            self.skipStepHandlerUI()
        elif (status == STEP_OK):
            self.stepOKHandlerUI()
            step.end()
        elif (status == STEP_KO):
            self.stepKOHandlerUI()
            step.end()
        elif (status == STEP_RETRY):
            step.end()
            time.sleep(1)
            # retry the same step
            self.stepIndex -= 1
        elif (status == RUN_TERMINATED):
            self.stepKOHandlerUI()
            step.end()
            # go to the last step, if we're not already on it
            if (self.stepIndex != (len(self.steps) - 1)):
                # XXX: the index will be incremented at the end of the function
                # thats why we have a `len() - 2` instead of a `len() - 1`
                self.stepIndex = len(self.steps) - 2
        else:
            step.end()
        self.stepIndex += 1

    # Check if stepName is non blocking
    def isNonBlockingStep(self, stepName):
        return stepName in self.nonBlockingSteps
