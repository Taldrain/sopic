from sopic.step import Step

class AlwaysKO(Step):
    STEP_NAME = 'Always KO'

    def start(self, _stepsData):
        super().start()

        return self.KO()
