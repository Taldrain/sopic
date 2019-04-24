from sopic.step import Step

class PrintSettings(Step):
    STEP_NAME = 'print-settings'

    def start(self, stepsData):
        super().start()

        self.logger.info('Random settings: {}'.format(stepsData['__settings']['random-settings']))

        return self.OK()
