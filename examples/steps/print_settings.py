from sopic.step import Step


class PrintSettings(Step):
    STEP_NAME = "print-settings"

    def start(self, ctx, settings, *kwargs):
        super().start()

        print("settings: ", settings)
        # TODO: use logger
        # self.logger.info(
        #     "Random settings: {}".format(stepsData["__settings"]["random-settings"])
        # )

        return self.OK()
