from sopic.step import Step

class AlwaysOK(Step):
    STEP_NAME = 'Always OK'

    def start(self, stepsData):
        super().start()

        return self.OK()
