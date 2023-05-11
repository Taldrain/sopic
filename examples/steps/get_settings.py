from sopic.step import Step


class GetSettings(Step):
    STEP_NAME = "get-settings"

    def start(self, ctx, settings, *kwargs):
        super().start()

        print(f"{settings['random-settings']=}")
        # TODO: use logger

        return self.OK()
