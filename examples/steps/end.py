from sopic.step import Step

class End(Step):
    STEP_NAME = 'end-step'

    def start(self, stepsData):
        super().start()

        self.logger.info("Has current run failed: {}".format("lastFailedStep" in stepsData['__status']))

        # Note that the current run is still in progress
        self.logger.info("Number of consecutive failed: {}".format(stepsData['__run']['consecutive_failed']))
        self.logger.info("Number of failed run / Number of run: {}/{}".format(
            stepsData['__run']['nb_failed'],
            stepsData['__run']['nb_run']
        ))

        return self.OK()
