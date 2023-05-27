from .gui import StepUI


#
# Step class
#
class Step:
    STEP_NAME = ""
    # Useful for flaky tests
    MAX_RETRIES = 0

    widget = None
    _childs = []

    def __init__(self, childs, logger):
        if len(self.STEP_NAME) == 0:
            raise NameError("STEP_NAME should be defined")

        if '.' in self.STEP_NAME:
            # Using a '.' might results in an incorrect display of the logs in
            # the logger widget. Only this handler parses and modifies the
            # logger name. See `WidgetFormatter` in the `utils/logger.py` file
            logger.warn("It is recommended to not use '.' in the STEP_NAME")

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
        self.logger.debug("Starting step")
        self.widget.clean()

    # Called when the step ends
    def end(self):
        self.logger.debug("Ending step")

    def buildStepResult(
            self,
            is_success,
            next_step_key=None,
            info_str=None,
            error_code=None,
        ):
        return {
            "isSuccess": is_success,
            "infoStr": info_str,
            "errorCode": error_code,
            "nextStepKey": next_step_key,
        }

    # The step has passed
    # stepData store data to be available for next steps
    def OK(self, next_step_key=None, info_str=""):
        log_str = "Step OK"
        if len(info_str) > 0:
            log_str += f" {info_str}"
        self.logger.info(log_str)
        return self.buildStepResult(
            True,
            next_step_key=next_step_key,
            info_str=info_str,
        )

    # The step has failed
    # stepData store data to be available for next steps
    # info_str store string about the step error
    # error_code store error code about the step error
    def KO(self, next_step_key=None, info_str="", error_code=None):
        log_str = "Step KO"
        if len(info_str) > 0:
            log_str += f" {info_str}"
        self.logger.error(log_str)
        return self.buildStepResult(
            False,
            next_step_key=next_step_key,
            info_str=info_str,
            error_code=error_code,
        )

    def getWidget(self):
        if self.widget is None:
            self.widget = StepUI()

        return self.widget
