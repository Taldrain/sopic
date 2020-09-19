from itertools import zip_longest

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from .step_status_widget import StepStatusWidget


# from https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, chunkSize, fillValue=None):
    # Collect data into fixed-length chunks or blocks
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * chunkSize
    return zip_longest(*args, fillvalue=fillValue)


def newHLayout(chunk):
    hlayout = QHBoxLayout()
    for widget in chunk:
        if widget is not None:
            hlayout.addWidget(widget)
    return hlayout


class RunViewerWidget(QWidget):
    # Number of StepStatusWidget per lines
    LINE_CHUNK_SIZE = 10

    def __init__(self, station, parent=None):
        super().__init__(parent)
        self.station = station

        self.childs = []

        for step in self.station.getSteps():
            self.childs.append(StepStatusWidget(step.getStepName()))

        vlayoutMain = QVBoxLayout()

        for chunk in grouper(
            self.childs, self.LINE_CHUNK_SIZE, fillValue=StepStatusWidget("")
        ):
            vlayoutMain.addLayout(newHLayout(chunk))

        self.setLayout(vlayoutMain)

    def updateCurrentTab(self):
        self.childs[self.station.getCurrentStep()].statusInProgress()

    def reset(self):
        for index, child in enumerate(self.childs):
            child.statusReset()
            # set background of skipped steps
            if not self.station.getSteps()[index].ACTIVATED:
                child.statusSkipped()

    def currentTabOK(self):
        self.childs[self.station.getCurrentStep()].statusOK()

    def currentTabKO(self):
        self.childs[self.station.getCurrentStep()].statusKO()

    def currentTabSkipped(self):
        self.childs[self.station.getCurrentStep()].statusSkipped()
