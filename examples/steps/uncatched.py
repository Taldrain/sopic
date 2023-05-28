from sopic.step import Step


class Uncatched(Step):
    STEP_NAME = "uncatched-step"

    def start(self, *kwargs):
        super().start()

        self.logger.warn("An exception in a previous step was not catched")

        return self.OK()
