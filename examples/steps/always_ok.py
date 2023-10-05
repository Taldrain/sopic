from sopic import Step


class AlwaysOK(Step):
    STEP_NAME = "Always OK"

    def start(self, *kwargs):
        super().start()

        return self.OK()
