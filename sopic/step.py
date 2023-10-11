from PySide6.QtWidgets import QWidget

#
# Step class
#
class Step(QWidget):
    STEP_NAME = ""
    # Useful for flaky tests
    MAX_RETRIES = 0

    _childs = []

    def __init__(self, childs, logger):
        super().__init__()
        if len(self.STEP_NAME) == 0:
            raise NameError("STEP_NAME should be defined")

        if "." in self.STEP_NAME:
            # Using a '.' might results in an incorrect display of the logs in
            # the logger widget. See `WidgetFormatter` in the `utils/logger.py`
            # file
            logger.warn("It is recommended to not use '.' in the STEP_NAME")

        self._childs = childs
        self.logger = logger

    # Try to access the step key using a child key
    # if `_childs` is a dict, we're trying to access the dictionary via a key
    # if `_childs` is an array, we're trying to access the array via an index
    # if nothing works, we returns `None`
    def get_step_key(self, key):
        if type(self._childs) is dict and key in self._childs:
            return self._childs[key]
        if type(key) is int and len(self._childs) > key:
            return self._childs[key]
        return None

    # Called when the step starts
    def start(self):
        self.logger.debug("Starting step")

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
    def OK(self, next_step_key=None, info_str=None):
        log_str = "Step OK"
        if info_str is not None:
            log_str += f" {info_str}"
        self.logger.info(log_str)
        return self.buildStepResult(
            True,
            next_step_key=next_step_key,
            info_str=info_str,
        )

    # The step has failed
    # `error_code` stores error code about the step error
    # `info_str` stores string about the step error
    def KO(self, next_step_key=None, info_str=None, error_code=None):
        log_str = "Step KO"
        if info_str is not None:
            log_str += f" {info_str}"
        self.logger.error(log_str)
        return self.buildStepResult(
            False,
            next_step_key=next_step_key,
            info_str=info_str,
            error_code=error_code,
        )
