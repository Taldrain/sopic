from .gui import StepUI


#
# Step class
#
class Step:
    # Useful for flaky tests
    MAX_RETRIES = 0
    STEP_NAME = ""

    widget = None
    _childs = []

    # XXX: We could remove stationName and stationID and force the use of
    # stepsData to retrieve them.
    def __init__(self, childs, logger):
        self._childs = childs
        self.logger = logger

    # XXX: comments
    def get_step_key(self, key):
        if type(self._childs) is dict and key in self._childs:
            return self._childs[key]
        if type(key) is int and len(self._childs) > key:
            return self._childs[key]
        return None

    # Called when the step starts
    def start(self):
        print(f'== [{self.STEP_NAME}] start')

        # self.logger.debug("Starting step " + self.STEP_NAME)

        self.widget.clean()

    # Called when the step ends
    def end(self):
        print(f'== [{self.STEP_NAME}] end')
        # self.logger.debug("Ending step " + self.STEP_NAME)

    def buildStepResult(self, is_success, next_step_key=None, infoStr=None, errorCode=None):
        return {
            "isSuccess": is_success,
            "infoStr": infoStr,
            "errorCode": errorCode,
            "nextStepKey": next_step_key,
        }

    # The step has passed
    # stepData store data to be available for next steps
    def OK(self, next_step_key=None, successStr=""):
        logStr = "OK step [" + self.STEP_NAME + "]"
        if len(successStr) > 0:
            logStr = logStr + " " + successStr
        # self.logger.info(logStr)
        return self.buildStepResult(True, next_step_key=next_step_key, infoStr=successStr)

    # The step has failed
    # stepData store data to be available for next steps
    # errorStr store string about the step error
    # errorCode store error code about the step error
    def KO(self, next_step_key=None, errorStr="", errorCode=None):
        logStr = "KO step [" + self.STEP_NAME + "]"
        if len(errorStr) > 0:
            logStr = logStr + " " + errorStr
        # self.logger.error(logStr)
        return self.buildStepResult(
            False,
            next_step_key=next_step_key,
            infoStr=errorStr,
            errorCode=errorCode
        )

    def getWidget(self):
        if self.widget is None:
            self.widget = StepUI()

        return self.widget
