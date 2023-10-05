from sopic.step import Step


class RetrieveData(Step):
    STEP_NAME = "retrieve-data"

    def start(self, ctx, *kwargs):
        super().start()

        # the "foo" key could be shared between the two steps via a specific
        # settings. Or it could be defined in the `Store` class as a static
        # field
        self.logger.info(f'{ctx["foo"]=}')

        return self.OK()
