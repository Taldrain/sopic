from sopic import Step

class DummyLogger():
    def debug(self, x):
        pass
    def info(self, x):
        pass
    def error(self, x):
        pass


def test_step_name():
    class CustomStep(Step):
        STEP_NAME = "custom-step"
    step = CustomStep("station_name", 42, None, True)
    assert step.getStepName() == "custom-step"

def test_step_ok():
    step = Step("station_name", 42, DummyLogger(), True)
    assert step.OK() == ({
        "passed": True,
        "stepData": {},
        "terminate": False,
        "infoStr": "",
        "errorCode": None,
    })

def test_step_ok_with_infostr():
    step = Step("station_name", 42, DummyLogger(), True)
    assert step.OK("infoStr") == ({
        "passed": True,
        "stepData": {},
        "terminate": False,
        "infoStr": "infoStr",
        "errorCode": None,
    })

def test_step_ko():
    step = Step("station_name", 42, DummyLogger(), True)
    assert step.KO() == ({
        "passed": False,
        "stepData": {},
        "terminate": False,
        "infoStr": "",
        "errorCode": None,
    })

def test_step_ko_terminate():
    step = Step("station_name", 42, DummyLogger(), True)
    assert step.KO(terminate=True) == ({
        "passed": False,
        "stepData": {},
        "terminate": True,
        "infoStr": "",
        "errorCode": None,
    })

def test_step_ko_errorCode():
    step = Step("station_name", 42, DummyLogger(), True)
    assert step.KO(errorCode=123) == ({
        "passed": False,
        "stepData": {},
        "terminate": False,
        "infoStr": "",
        "errorCode": 123,
    })

def test_step_ko_errorStr():
    step = Step("station_name", 42, DummyLogger(), True)
    assert step.KO(errorStr="foo") == ({
        "passed": False,
        "stepData": {},
        "terminate": False,
        "infoStr": "foo",
        "errorCode": None,
    })

def test_step_ko_fulle():
    step = Step("station_name", 42, DummyLogger(), True)
    assert step.KO(terminate=True, errorCode=123, errorStr="foo") == ({
        "passed": False,
        "stepData": {},
        "terminate": True,
        "infoStr": "foo",
        "errorCode": 123,
    })
