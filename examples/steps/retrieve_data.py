from sopic.step import Step


class RetrieveData(Step):
    STEP_NAME = "retrieve-data"

    def start(self, ctx, *kwargs):
        super().start()

        self.logger.info(f'{ctx["foo"]=}')

        return self.OK()
