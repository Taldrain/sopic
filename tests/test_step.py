from sopic import Step


class DummyLogger:
    def debug(self, x):
        pass

    def info(self, x):
        pass

    def warn(self, x):
        pass

    def error(self, x):
        pass

    def critical(self, x):
        pass


class DummyStep(Step):
    STEP_NAME = "dummy-step"


def test_step_name():
    class CustomStep(Step):
        STEP_NAME = "custom-step"

    step = CustomStep([], None)
    assert step.STEP_NAME == "custom-step"


def test_step_ok():
    step = DummyStep([], DummyLogger())
    assert step.OK() == (
        {
            "isSuccess": True,
            "infoStr": "",
            "errorCode": None,
            "nextStepKey": None,
        }
    )


def test_step_ok_info_str():
    step = DummyStep([], DummyLogger())
    assert step.OK(info_str="infoStr") == (
        {
            "isSuccess": True,
            "infoStr": "infoStr",
            "errorCode": None,
            "nextStepKey": None,
        }
    )


def test_step_ok_next_step_key():
    step = DummyStep([], DummyLogger())
    assert step.OK(next_step_key="foo") == (
        {
            "isSuccess": True,
            "infoStr": "",
            "errorCode": None,
            "nextStepKey": "foo",
        }
    )


def test_step_ko():
    step = DummyStep([], DummyLogger())
    assert step.KO() == (
        {
            "isSuccess": False,
            "infoStr": "",
            "errorCode": None,
            "nextStepKey": None,
        }
    )


def test_step_ko_error_code():
    step = DummyStep([], DummyLogger())
    assert step.KO(error_code=123) == (
        {
            "isSuccess": False,
            "infoStr": "",
            "errorCode": 123,
            "nextStepKey": None,
        }
    )


def test_step_ko_info_str():
    step = DummyStep([], DummyLogger())
    assert step.KO(info_str="foo") == (
        {
            "isSuccess": False,
            "infoStr": "foo",
            "errorCode": None,
            "nextStepKey": None,
        }
    )


def test_step_ko_full():
    step = DummyStep([], DummyLogger())
    assert step.KO(info_str="foo", error_code=42, next_step_key="bar") == (
        {
            "isSuccess": False,
            "infoStr": "foo",
            "errorCode": 42,
            "nextStepKey": "bar",
        }
    )
