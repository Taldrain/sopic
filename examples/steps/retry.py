from time import sleep
from random import randint

from sopic.step import Step
from sopic.gui import StepUI

class Retry(Step):
    STEP_NAME = 'retry'
    MAX_RETRIES = 3

    def start(self, stepsData):
        super().start()

        if (randint(0, 4) != 0):
            return self.KO()

        return self.OK()
