from sopic.step import Step


class PrintSettings(Step):
    STEP_NAME = "print-settings"

    # `ctx` contains variables previous steps of the run may have set
    # `settings` contains the settings of the station
    def start(self, ctx, settings, *kwargs):
        super().start()

        self.logger.info(f"All settings of the station: {settings}")

        return self.OK()
