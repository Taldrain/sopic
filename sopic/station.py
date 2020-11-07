import os
import json
import time
import datetime
import pygraphviz as pgv

from .utils import getLogger

STEP_SKIPPED = "skipped"
STEP_RETRY = "retry"
STEP_OK = "ok"
STEP_KO = "ko"
RUN_TERMINATED = "terminated"


#
# Station class
#
class Station:
    # Should be overwritten by child
    DISPLAY_NAME = ""
    STATION_NAME = ""
    STATION_ID = 0
    STATION_VERSION = None

    # list of steps name that will not steps the current run
    # by default a failure end the run
    nonBlockingSteps = []

    # list of steps name that should be skip if a previous step (a non blocking
    # step) has failed
    stepsSkippedOnPreviousFail = []

    # Id of the previous station, checked at the start of the run
    # None to disable the check
    previousStationId = None

    # StepsData available for all steps, and defined in the child stations
    # Used for data shared between multiple steps
    defaultStepsData = {}
    stepsData = {}

    defaultSettings = {}
    settings = None

    # path to logs file, if enabled
    defaultLogDir = "~/.sopic/logs/"

    # should the log to file be enabled
    disableFileLogging = False

    # disable all logger handlers
    disableLogHandlers = False

    # allow to add other handlers
    logHandlers = []

    # path to settings file
    defaultSettingsDir = "~/.sopic/settings/"

    # optional password for the step and settings dialogs
    adminPassword = None

    # Optional steps that will be used before and after a run
    # They can be use to display a start/end button. Using those steps allow
    # the station to use the startRunHandler and endRunHandler closer to the
    # run.
    #
    # Example: if the last step of the array of steps was used to display a
    # button to finish the current run and the status of the run (pass or fail).
    # The operator might close the station or leave the station on this screen
    # thinking the run was completed. But if the station was using the method
    # endRunHandler, it will never be called.
    # Creating a separation for the run and other operations (start/end run
    # buttons or pass/fail information) allow us to use the startRunHandler
    # and endRunHandler.
    startStep = None
    endStep = None

    steps = []

    # nextStepHandler: handler called when a new step start
    # clearStepsHandlerUI: handler called when starting a new run
    # stepOKHandler: handler called when a step is OK
    # stepKOHandler: handler called when a step is KO
    def __init__(
        self,
        nextStepHandlerUI=None,
        clearStepsHandlerUI=None,
        stepOKHandlerUI=None,
        stepKOHandlerUI=None,
        skipStepHandlerUI=None,
        endRunHandlerUI=None,
        forceStepHandlerUI=None,
    ):
        self.logger = getLogger(
            self.STATION_NAME,
            self.STATION_ID,
            self.disableFileLogging,
            self.defaultLogDir,
            self.logHandlers,
            self.disableLogHandlers,
        )

        self.steps = list(map(self._initStep, self.steps))
        if self.startStep is not None:
            self.startStep = self._initStep(self.startStep)
        if self.endStep is not None:
            self.endStep = self._initStep(self.endStep)

        self.stepIndex = 0

        self.nextStepHandlerUI = nextStepHandlerUI
        self.clearStepsHandlerUI = clearStepsHandlerUI
        self.stepOKHandlerUI = stepOKHandlerUI
        self.stepKOHandlerUI = stepKOHandlerUI
        self.skipStepHandlerUI = skipStepHandlerUI
        self.endRunHandlerUI = endRunHandlerUI
        self.forceStepHandlerUI = forceStepHandlerUI

        self.settingsPath = os.path.join(
            os.path.expanduser(self.defaultSettingsDir),
            self.STATION_NAME + ".json",
        )

        if self.defaultSettings is not None:
            self._readSettingFile()

        # first init of stepsData object
        self._initStepData()

        self.logger.debug("Starting station")

    # stepDef is the step from the step array defined in a station.py file.
    # It can, sometimes, be a tuple (step, boolean) to overwrite the ACTIVATED
    # flag of the step.
    def _initStep(self, stepDef):
        if isinstance(stepDef, tuple):
            return stepDef[0](
                self.STATION_NAME,
                self.STATION_ID,
                self.logger,
                stepDef[1] is not False,
            )
        return stepDef(self.STATION_NAME, self.STATION_ID, self.logger, True)

    def _readSettingFile(self):
        self.settings = self.defaultSettings.copy()
        try:
            with open(self.settingsPath) as settingsRaw:
                settingsData = json.load(settingsRaw)
                self.settings.update(settingsData)
        except Exception:
            return

    def getEmptyStepsData(self):
        return {
            **self.defaultStepsData,
            **{
                "__status": {
                    "id": self.STATION_ID,
                    "name": self.STATION_NAME,
                    "previousStationId": self.previousStationId,
                },
                "__settings": self.settings,
                "__errors": [],
                "__run": {
                    "success": True,
                    "consecutive_failed": 0,
                    "nb_failed": 0,
                    "nb_run": 0,
                },
            },
        }

    def _initStepData(self):
        self.stepsData = self.getEmptyStepsData()

    # clean previous step data, the __run object will be updated
    # after the, optional, startStep
    def _cleanStepData(self):
        self.stepsData = {
            **(self.getEmptyStepsData()),
            "__run": {
                **self.stepsData["__run"],
            },
        }

    def _updateRunStepData(self):
        self.stepsData["__run"]["startDate"] = datetime.datetime.utcnow()

    def updateValueSettings(self, key, value):
        self.settings[key] = value
        self.stepsData["__settings"] = self.settings

    # Dump the settings into a file
    def updateSettingsFile(self):
        os.makedirs(os.path.dirname(self.settingsPath), exist_ok=True)

        with open(self.settingsPath, "w") as file:
            json.dump(self.settings, file)

    # Resets the settings of the station by removing the local file
    # and re-setting the settings variable
    def resetSettings(self):
        try:
            os.remove(self.settingsPath)
        except OSError:
            pass
        # TODO is self.settings used ?
        # we could just used __settings
        self.settings = self.defaultSettings.copy()
        self.stepsData["__settings"] = self.settings

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

            self._cleanStepData()
            # Optional step for display/interaction
            if self.startStep is not None:
                self.forceStepHandlerUI(len(self.steps), clearRunViewer=True)
                # stepResult is skipped
                self.startStep.start(self.stepsData)

            self.startRunHandler()
            # The run has now started
            isSuccessRun = self.run()
            # The run is now over
            self.endRunHandler(isSuccessRun)

            # Optional step for display/interaction
            if self.endStep is not None:
                self.forceStepHandlerUI(
                    len(self.steps) + (1 if self.startStep is not None else 0)
                )
                # stepResult is skipped
                self.endStep.start(self.stepsData)

    # Start a run
    def run(self):
        numberRetries = 0

        isSuccessRun = True

        # Iterate on all steps
        while self.stepIndex < len(self.steps):
            step = self.steps[self.stepIndex]

            self.nextStepHandlerUI()

            # Skip the step, it's been deactivated
            if step.ACTIVATED is False:
                self.logger.warning(
                    "Skipping step {} - the step has been deactivated".format(
                        step.STEP_NAME
                    )
                )
                self.endStepHandler(STEP_SKIPPED, step, {})
                continue

            # Skip the step, a previous step has failed and this step is tagged as skip on fail
            if step.STEP_NAME in self.stepsSkippedOnPreviousFail and not isSuccessRun:
                self.logger.error(
                    "Skipping step {} - a previous step has failed".format(
                        step.STEP_NAME
                    )
                )
                self.endStepHandler(STEP_SKIPPED, step, {})
                continue

            try:
                # Run the step
                stepResult = step.start(self.stepsData)
            except Exception as e:
                # Catch any non-catched exception with a default errorCode
                # The run is also terminated
                stepResult = step.buildStepResult(False, True, str(e), 255)
                self.logger.error(
                    "Exception not catch in step {}: {}".format(step.STEP_NAME, e)
                )

            # The step has passed
            if stepResult["passed"]:
                # Save the stepData object
                self.stepsData[step.STEP_NAME] = stepResult["stepData"]
                self.endStepHandler(STEP_OK, step, stepResult)
                # Reset the number of retries
                numberRetries = 0
            else:
                # The step has failed

                # Track if the step has terminated
                if stepResult["terminate"]:
                    self.stepsData["__status"]["terminated"] = True

                # If the step has not reach its max number of retries,
                # we will relaunch the same step on the next loop iteration
                if step.MAX_RETRIES != 0 and numberRetries < step.MAX_RETRIES:
                    numberRetries += 1
                    self.logger.info("Retrying step")
                    self.endStepHandler(STEP_RETRY, step, stepResult)
                    continue

                # The max number of retries is reached, or the step has no retry
                isSuccessRun = False
                numberRetries = 0
                # Track the name of the last step that has failed
                # Can be used to track the run status
                self.stepsData["__status"]["lastFailedStep"] = step.STEP_NAME
                self.stepsData[step.STEP_NAME] = stepResult["stepData"]
                # When an errorCode is available, store it in the __errors array
                if stepResult["errorCode"] is not None:
                    self.stepsData["__errors"].append(
                        (
                            step.STEP_NAME,
                            stepResult["errorCode"],
                            stepResult["infoStr"],
                        )
                    )

                # The step is non blocking, and the station is not in a terminate run
                if (
                    self.isNonBlockingStep(step.STEP_NAME)
                    and stepResult["terminate"] is False
                ):
                    # The step has failed, but the station will start the next step
                    self.logger.debug("Non-Blocking step reached")
                    self.endStepHandler(STEP_KO, step, stepResult)
                else:
                    # Blocking step, or terminate run, the station will go to the last step
                    self.logger.debug("Blocking step reached, go to last step")
                    self.endStepHandler(RUN_TERMINATED, step, stepResult)

        return isSuccessRun

    # handler of the start run
    def startRunHandler(self):
        self._updateRunStepData()
        self.clearStepsHandlerUI()
        self.logger.info("Starting run")

    # handler of end step
    #
    # TODO we could simplify by merging some statements
    # -> update ui (OK, KO, retry)
    # -> update the step (step.end())
    # -> update the index
    #   - we could also rework how the index is dealt, we could replace the
    #     `while` loop with a `for` loop and prevent any manual update of the
    #     index.
    #     We would just have to track a "terminated" run to skip the step.
    #     Having a dedicated end run step would also be cleaner, insted of
    #     having to run the last step, even in terminated run.
    def endStepHandler(self, status, step, stepResult):
        if status == STEP_SKIPPED:
            self.skipStepHandlerUI()
        elif status == STEP_OK:
            self.stepOKHandlerUI()
            step.end()
        elif status == STEP_KO:
            self.stepKOHandlerUI()
            step.end()
        elif status == STEP_RETRY:
            step.end()
            time.sleep(1)
            # retry the same step
            self.stepIndex -= 1
        elif status == RUN_TERMINATED:
            self.stepKOHandlerUI()
            step.end()
            # go to the last step, if we're not already on it
            if self.stepIndex != (len(self.steps) - 1):
                # XXX: the index will be incremented at the end of the function
                # thats why we have a `len() - 2` instead of a `len() - 1`
                self.stepIndex = len(self.steps) - 2
        else:
            step.end()
        self.stepIndex += 1

    # handler of the end run
    def endRunHandler(self, isSuccessRun):
        # Saving the start run date, it will be clear when we update the stepsData
        startRunDate = self.stepsData["__run"]["startDate"]

        # update stepsData for current run

        self.stepsData["__run"]["success"] = isSuccessRun
        self.stepsData["__run"]["consecutive_failed"] = (
            self.stepsData["__run"]["consecutive_failed"] + 1
            if (not isSuccessRun)
            else 0
        )
        self.stepsData["__run"]["nb_run"] = self.stepsData["__run"]["nb_run"] + 1

        nbFailed = self.stepsData["__run"]["nb_failed"]
        self.stepsData["__run"]["nb_failed"] = (
            nbFailed + 1 if (not isSuccessRun) else nbFailed
        )

        self.endRunHandlerUI(self.stepsData["__run"])
        self.logger.debug(
            "Run took {}s".format((datetime.datetime.utcnow() - startRunDate).seconds)
        )
        self.logger.info(
            "Run ended with a {}".format(("SUCCESS" if isSuccessRun else "FAIL"))
        )
        self.logger.info("Ending run ---------------------------------------")

    # Check if stepName is non blocking
    def isNonBlockingStep(self, stepName):
        return stepName in self.nonBlockingSteps

    def writeWorkflow(self):
        graph = pgv.AGraph(strict=False)

        # not really clear to use the index, what about the start/stop steps
        def nodeId(index):
            return "{}-{}".format(index, self.steps[index].STEP_NAME)

        def createNode(index):
            graph.add_node(nodeId(index), label=self.steps[index].STEP_NAME)

        def createEdge(a, b, label):
            graph.add_edge(a, b, label=label, dir="forward")

        for index, step in enumerate(self.steps):
            createNode(index)

            if index > 0:
                if (index < len(self.steps) - 1) and (
                    step.STEP_NAME in self.stepsSkippedOnPreviousFail
                ):
                    createEdge(nodeId(index - 1), nodeId(index + 1), "Skip")
                elif self.steps[index - 1].STEP_NAME in self.nonBlockingSteps:
                    createEdge(nodeId(index - 1), nodeId(index), "KO")
                else:
                    createEdge(
                        nodeId(index - 1), nodeId(len(self.steps) - 1), "Terminate"
                    )

                createEdge(nodeId(index - 1), nodeId(index), "OK")

            if self.steps[index].MAX_RETRIES > 0:
                createEdge(
                    nodeId(index),
                    nodeId(index),
                    "Retries {}x".format(self.steps[index].MAX_RETRIES),
                )

        if self.startStep is not None:
            createEdge(self.startStep.STEP_NAME, nodeId(0), "Start")

        lastStepId = nodeId(len(self.steps) - 1)
        if self.endStep is not None:
            createEdge(lastStepId, self.endStep.STEP_NAME, "End")
            lastStepId = self.endStep.STEP_NAME

        graph.add_node("OK", style="filled", fillcolor="green")
        graph.add_node("KO", style="filled", fillcolor="red")

        createEdge(lastStepId, "KO", "")
        createEdge(lastStepId, "OK", "")

        graph.write("workflow.dot")
