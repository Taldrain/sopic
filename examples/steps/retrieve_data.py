from sopic.step import Step
from sopic.gui import StepUI

from . import StoreData

class RetrieveData(Step):
    STEP_NAME = 'retrieve-data'

    def start(self, stepsData):
        super().start()

        self.logger.info("Retrieve data from {} step: {}".format(
            StoreData.STEP_NAME,
            stepsData[StoreData.STEP_NAME][StoreData.EXPORTED_KEY]
        ))

        return self.OK()
