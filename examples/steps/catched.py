from sopic.step import Step


class Catched(Step):
    STEP_NAME = "catched-step"

    def start(self, *kwargs):
        super().start()

        return self.OK()
