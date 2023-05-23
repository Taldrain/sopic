from sopic.step import Step


class End(Step):
    STEP_NAME = "end-step"

    def start(self, ctx, settings, run_info):
        super().start()

        # TODO switch to logger
        print(f"The run {'succeded' if run_info['run']['last_failed_step'] is None else 'failed'}")

        return self.OK()
