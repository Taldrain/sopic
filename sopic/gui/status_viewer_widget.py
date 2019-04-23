from itertools import zip_longest

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from . import StatusElementWidget

# from https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, chunkSize, fillValue=None):
    # Collect data into fixed-length chunks or blocks
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * chunkSize
    return zip_longest(*args, fillvalue=fillValue)



class StatusViewerWidget(QWidget):
    # Number of StatusElementWidget per lines
    LINE_CHUNK_SIZE = 10

    def __init__(self, station, parent=None):
        super().__init__(parent)
        self.station = station
        self.current_index = self.station.getCurrentStep()
        self.init_gui()

    def init_gui(self):
        self.init_widgets()
        vlayoutMain = QVBoxLayout()

        for chunk in grouper(self.childs, self.LINE_CHUNK_SIZE, fillValue=StatusElementWidget('')):
            vlayoutMain.addLayout(self.new_hlayout(chunk))

        self.setLayout(vlayoutMain)

    def new_hlayout(self, chunk):
        hlayout = QHBoxLayout()
        for widget in chunk:
            if (widget is not None):
                hlayout.addWidget(widget)
        return hlayout

    def init_widgets(self):
        self.childs = []

        for step in self.station.getSteps():
            self.childs.append(StatusElementWidget(step.getStepName()))

        self.childs[0].in_progress()

    def update_current_tab(self):
        new_index = self.station.getCurrentStep()
        self.childs[new_index].in_progress()

    def reset(self):
        for index, child in enumerate(self.childs):
            child.reset()
            # set background of skipped steps
            if (not self.station.getSteps()[index].ACTIVATED):
                child.skipped()

    def current_tab_ok(self):
        self.childs[self.station.getCurrentStep()].ok()

    def current_tab_skipped(self):
        self.childs[self.station.getCurrentStep()].skipped()

    def current_tab_ko(self):
        self.childs[self.station.getCurrentStep()].ko()
