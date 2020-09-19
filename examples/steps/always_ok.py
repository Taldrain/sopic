from sopic.step import Step


class AlwaysOK(Step):
    STEP_NAME = "Always OK"

    def start(self, _stepsData):
        super().start()

        return self.OK()
