from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QSplitter
)

from PyQt5.QtCore import Qt

import threading

from . import LoggerWidget
from . import TabManagerWidget
from . import RunViewerWidget
from . import SettingsViewerWidget
from . import StepSelectionDialog
from . import StationStatusWidget

class MainWindow(QMainWindow):
    settings_dialog = None
    debugDisplay = False
    def __init__(self, station, settings_dialog=None):
        super().__init__()
        self.station = station(
            nextStepHandlerUI = self.nextStepHandlerUI,
            clearStepsHandlerUI = self.clearStepsHandlerUI,
            stepOKHandlerUI = self.stepOKHandlerUI,
            stepKOHandlerUI = self.stepKOHandlerUI,
            skipStepHandlerUI = self.skipStepHandlerUI,
            endRunHandler = self.endRunHandler
        )

        if (settings_dialog is not None):
            self.settings_dialog = settings_dialog(
                self.station,
                self.station.updateValueSettings,
                self.station.updateSettingsFile,
                self.station.resetSettings
            )

        self.step_selection_dialog = StepSelectionDialog(
                self.station.steps
        )

        self.init_gui()

        self.worker_thread = threading.Thread(target=self.start)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def init_gui(self):
        self.init_widgets()
        center_widget = QWidget()

        vlayoutMain = QVBoxLayout()
        hlayoutChild = QHBoxLayout()

        vlayoutMain.addWidget(self.run_viewer_widget)
        vlayoutMain.addWidget(self.station_status_widget)

        self.splitter.addWidget(self.tab_manager_widget)
        self.splitter.addWidget(self.logger_widget)

        hlayoutChild.addWidget(self.splitter)

        if (self.settings_dialog is not None):
            hlayoutChild.addWidget(self.settings_viewer_widget)

        vlayoutMain.addLayout(hlayoutChild)
        vlayoutMain.setStretchFactor(hlayoutChild, 60)

        center_widget.setLayout(vlayoutMain)
        self.setCentralWidget(center_widget)
        self.setMinimumSize(640, 480)
        self.setWindowTitle(self.station.getDisplayName())

    def init_widgets(self):
        self.logger_widget = LoggerWidget(self)
        self.station.logger.addHandler(self.logger_widget)
        self.splitter = QSplitter()
        self.tab_manager_widget = TabManagerWidget(self.station)
        self.station_status_widget = StationStatusWidget()
        self.run_viewer_widget = RunViewerWidget(self.station)
        if (self.settings_dialog is not None):
            self.settings_viewer_widget = SettingsViewerWidget(self.station)
            self.settings_dialog.accepted.connect(self.settings_viewer_widget.slot_update)
        self.updateLayoutDebug()

    def updateLayoutDebug(self):
        if self.debugDisplay:
            self.logger_widget.show()
            if (self.settings_dialog):
                self.settings_viewer_widget.show()
        else:
            self.logger_widget.hide()
            if (self.settings_dialog):
                self.settings_viewer_widget.hide()

    def start(self):
        self.station.start()

    def nextStepHandlerUI(self):
        self.tab_manager_widget.update_current_tab()
        self.run_viewer_widget.update_current_tab()

    def skipStepHandlerUI(self):
        self.run_viewer_widget.current_tab_skipped()

    def clearStepsHandlerUI(self):
        self.run_viewer_widget.reset()
        # we re-update the current tab, it was cleaned with the previous reset
        self.run_viewer_widget.update_current_tab()

    def stepOKHandlerUI(self):
        self.run_viewer_widget.current_tab_ok()

    def stepKOHandlerUI(self):
        self.run_viewer_widget.current_tab_ko()

    def endRunHandler(self, runObj):
        self.station_status_widget.update(runObj)

    def keyPressEvent(self, event):
        k = event.key()

        # Quit via Escape or Ctrl-C
        if (k == Qt.Key_Escape) or (k == Qt.Key_Q and
            (QApplication.keyboardModifiers() & Qt.ControlModifier)):
            self.close()

        # Settings via Ctrl-H
        if ((QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_H)):
            if (self.settings_dialog):
                self.settings_dialog.show()

        # Step selection via Ctrl-T
        if ((QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_T)):
            self.step_selection_dialog.show()

        # Debug layout via Ctrl-D
        if ((QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_D)):
            self.debugDisplay = not self.debugDisplay
            self.updateLayoutDebug()
