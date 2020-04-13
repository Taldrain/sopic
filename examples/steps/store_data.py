from random import randint

from sopic.step import Step

class StoreData(Step):
    STEP_NAME = 'store-data'
    EXPORTED_KEY = 'random-value'

    def start(self, _stepsData):
        super().start()

        randomValue = randint(0, 9)
        self.logger.info("Storing random value: {}".format(randomValue))

        # Note that 'self.stepData' is different from 'stepsData'
        self.stepData[self.EXPORTED_KEY] = randomValue

        return self.OK()
