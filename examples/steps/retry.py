from random import randint

from sopic.step import Step


class Retry(Step):
    STEP_NAME = "retry"
    # 3 retries, this step can be run 4 times in total if it fails
    MAX_RETRIES = 3

    def start(self, *kwargs):
        super().start()

        if randint(0, 4) != 0:
            return self.KO()

        return self.OK()
