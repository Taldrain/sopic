from sopic.step import Step


class PrintSettings(Step):
    STEP_NAME = "print-settings"

    def start(self, ctx, settings, *kwargs):
        super().start()

        self.logger.info(f"Settings of the station: {settings}")

        return self.OK()
