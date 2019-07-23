from .gui import StepUI

#
# Step class
#
class Step:
    widget = None
    stepData = {}
    # Useful for flaky tests
    MAX_RETRIES = 0
    ACTIVATED = True

    # XXX: We could remove stationName and stationID and force the use of
    # stepsData to retrieve them.
    def __init__(self, stationName, stationID, logger, activated):
        self.ACTIVATED = activated
        self.stationName = stationName
        self.stationID = stationID
        self.logger = logger

    def getStepName(self):
        return self.STEP_NAME

    # Called when the step starts
    def start(self):
        self.logger.debug("Starting step " + self.STEP_NAME)
        self.stepData = {}

        self.widget.clean()

    # Called when the step ends
    def end(self):
        self.logger.debug("Ending step " + self.STEP_NAME)

    def buildStepResult(self, passed, terminate = False, infoStr = None, errorCode = None, resultObj = None):
        return {
            "passed": passed,
            "stepData": self.stepData,
            "terminate": terminate,
            "infoStr": infoStr,
            "errorCode": errorCode,
            "resultObj": resultObj,
        }

    # The step has passed
    # stepData store data to be available for next steps
    # resultObj allow the caller to store other data about the test
    #   eg, if comparing a value, the thresholds could be saved to be stored in a log system
    def OK(self, successStr = "", resultObj = None):
        logStr = "OK step [" + self.STEP_NAME + "]"
        if (len(successStr) > 0):
            logStr = logStr + " " + successStr
        self.logger.info(logStr)
        return self.buildStepResult(True, infoStr=successStr, resultObj = None)

    # The step has failed
    # stepData store data to be available for next steps
    # terminate force the station to end after this step
    # errorStr store string about the step error
    # errorCode store error code about the step error
    # resultObj allow the caller to store other data about the test
    def KO(self, terminate = False, errorStr = "", errorCode = None, resultObj = None):
        logStr = "KO step [" + self.STEP_NAME + "]"
        if (len(errorStr) > 0):
            logStr = logStr + " " + errorStr
        self.logger.error(logStr)
        return self.buildStepResult(False, terminate=terminate, infoStr=errorStr, errorCode=errorCode, resultObj=resultObj)

    def getWidget(self):
        if (self.widget == None):
            self.widget = StepUI()

        return self.widget
