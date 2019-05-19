FeetMe Sopic
============

Helper library for a test station in a production line.

Define a station that will run a number of steps, in sequential order.


# Screenshots

// TODO


# Installation

`pip install --user -e .`


# How to use

Initialise a `MainWindow` with a station object, child of the `Station` class.

In your station class you can set some parameters and define your list of steps.

You can also define a settings dialog when initializing the `MainWindow`.

Check the examples directory.

# Keybinds

### Exit the station
Escape or Ctrl-C

### Settings
**Ctrl-H**

DIsplay the settings dialog. The configuration is saved. The settings can be
reset to the default configuration set in the station class.

### Step selection
**Ctrl-T**

Allow to enable/disable steps. The configuration is not saved.

### Debug layout
**Ctrl-D**

Display settings and log window


# Definitions

A step is the smallest component, a class invoked at the start of the station.
A method from this object will be called to start the step. The step has then
access to data from previous steps, if they provided it, and global settings of
the station.
After being called, the step has to notify the station of the tests passed or
not.

A station is a group of steps. It's also defined as a class and will store the
default settings, station configuration and the steps.

A run is the term used to define the "list" of steps from the first to the last,
as defined in the station class.
So a station will perform multiple runs. Each one composed of multiple steps.


# Features

- GUI
- Share data between steps
- Settings for step configuration
- Step selection
- Logs

# Define a station

```python
from sopic import Station

class MyStation(Station):
    # Used as window title
    DISPLAY_NAME = 'my station'
    # Used for logs, filenames
    STATION_NAME = 'my-station'
    # Same use as STATION_NAME, useful to when saving the previous station
    STATION_ID = 0

    # Allow to disable logging to files
    disable_file_logging = False

    # List of steps in the station
    steps = [
      Step1,
      # Can deactivate step by default
      # steps can be enabled with the step selection dialog
      (Step2, False),
    ]

    # By default a fail in a step will force the run to go directly to the
    # last step, skipping other steps.
    # By defining the non blocking steps we allow the run to continue even
    # if these steps failed. Useful when testing the station without caring
    # about the step output
    # Note that the run is still a fail if one of these steps fail.
    nonBlockingSteps = [
      Step1.STEP_NAME,
    ]

    # Steps that will always be skipped if one previous step has failed.
    # Useful when also using nonBlockingSteps
    stepsSkippedOnPreviousFail = [
      Step2.STEP_NAME,
    ]

    # Default settings of the station. Can be updated with the SettingsDialog.
    defaultSettings = {
      'random-setting': '42',
    }
```

# Define a step

```python
from sopic import Step

class MyStep(Step):
    # name of the step, used for display and logs
    STEP_NAME = 'my-step'
    # number of retries allowed on fail
    MAX_RETRIES = 1

    # called when the step is started
    # stepsData contains data of the previous steps, if available.
    # Data of steps is available via `stepsData[Step1.STEP_NAME]`.
    # Settings is available at `stepsData['__settings']`.
    # Check the End step in the example folder for more use of the stepsData.
    def start(self, stepsData):
        super().start()

        # Add your tests here
        # You have access to `self.logger` to log some info.
        # You have access to the object `self.stepData` to store data, it will
        # be available for future the next steps. This object is reset on each run.
        # The step will have to return either `OK` or `KO`

        # A string can be passed to describe the success of the step.
        return self.OK('all good')

        # On error, the step should return `self.KO`
        # terminate, flag will force the run to end.
        # errorStr and errorCode is used to describe the error
        # return self.KO(
            terminate = False,
            errorStr = "something happened",
            errorCode = 42
        )

    # Used if the step define use a StepUI
    # Check the steps in the examples directory
    def getWidget(self):
        if (self.widet === None):
            self.widget = MyStepUI()
        return self.widget
```


# Examples

[Check the examples directory](./examples)


# TODO

_unordered_

- [ ] improve API documentation
- [ ] proper tests
- [ ] rework log format, they should be parseable
- [ ] cleaner step definition (nonblocking/skipped/clean or ending step)
- [ ] rework the main station loop, we should use a for-loop and not having to manually update the stepIndex
- [ ] feature to freeze the settings and steps

# See also

[exclave](https://github.com/exclave/exclave)
[Exclave: Hardware Testing in Mass Production, Made Easier](https://www.bunniestudios.com/blog/?p=5450)
