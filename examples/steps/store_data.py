from random import randint

from sopic.step import Step
from sopic.gui import StepUI

class StoreData(Step):
    STEP_NAME = 'store-data'
    EXPORTED_KEY = 'random-value'

    def start(self, stepsData):
        super().start()

        randomValue = randint(0, 9)
        self.logger.info("Storing random value: {}".format(randomValue))
        self.stepData[self.EXPORTED_KEY] = randomValue

        return self.OK()
