from sopic.step import Step


class GetSettings(Step):
    STEP_NAME = "get-settings"

    def start(self, ctx, settings, *kwargs):
        super().start()

        self.logger.info(f"{settings['random-settings']=}")

        return self.OK()
