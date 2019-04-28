FeetMe Sopic
============

Helper library for a test station in a production line

Define a station that will run a number of steps, in sequential order. A run
as a start and an end.


# Screenshots

// TODO

# Requirement

The project will require

- pyqt5
- python-colorlog

All the dependencies will be installed during the installation.


# Installation

`pip install --user -e .`


# How to use

Initialise a `MainWindow` with a station object, child of the `Station` class.

In your station class you can set some parameters and define your list of steps.

You can also define a settings dialog when initializing the `MainWindow`.

Check the examples directory.


# Definitions

A step is the smallest component, a class invoked at the start of the station.
A method from this object will be called to start the step. The step has then
access to data from previous step, if they provided it, and global settings of
the station.
After being called, the step has to notify the station of it's correct or
incorrect status.

Station
// TODO

A run is the term used to define the "list" of steps from the first to the last,
as defined in the station class.
So a station will perform multiple runs. Each one composed of multiple steps.


# Features

GUI

Share data between steps

Options

Logs


# API

## Step

### STEP_NAME

### OK

### KO

### Retry

### StepUI

### stepData object

### stepsData object


## Station

### STATION_ID/STATION_NAME

### Steps

### Non blocking steps

### Step skipped

### Settings

### Paths

### Error object

### 


# Examples


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
