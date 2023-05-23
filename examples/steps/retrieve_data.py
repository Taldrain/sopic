from sopic.step import Step


class RetrieveData(Step):
    STEP_NAME = "retrieve-data"

    def start(self, ctx, *kwargs):
        super().start()

        # TODO: use logger
        print(f'{ctx["foo"]=}')

        return self.OK()
