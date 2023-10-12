from sopic.step import Step


class AlwaysKO(Step):
    STEP_NAME = "Always KO"

    def start(self, *kwargs):
        super().start()

        return self.KO()
