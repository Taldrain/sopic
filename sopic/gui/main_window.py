import threading

from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QSplitter,
)

from PyQt5.QtCore import Qt

from .logger_widget import LoggerWidget
from .tab_manager_widget import TabManagerWidget
from .run_viewer_widget import RunViewerWidget
from .settings_viewer_widget import SettingsViewerWidget
from .step_selection_dialog import StepSelectionDialog
from .station_status_widget import StationStatusWidget
from .station_info_widget import StationInfoWidget
from .password_dialog import PasswordDialog


class MainWindow(QMainWindow):
    settingsDialog = None
    passwordDialog = None
    splitter = None

    loggerWidget = None
    tabManagerWidget = None
    stationStatusWidget = None
    runViewerWidget = None
    settingsViewerWidget = None
    stationInfoWidget = None

    debugDisplay = False

    def __init__(self, station, settingsDialog=None):
        super().__init__()
        self.station = station(
            nextStepHandlerUI=self.nextStepHandlerUI,
            clearStepsHandlerUI=self.clearStepsHandlerUI,
            stepOKHandlerUI=self.stepOKHandlerUI,
            stepKOHandlerUI=self.stepKOHandlerUI,
            skipStepHandlerUI=self.skipStepHandlerUI,
            endRunHandlerUI=self.endRunHandlerUI,
            forceStepHandlerUI=self.forceStepHandlerUI,
        )

        if settingsDialog is not None:
            self.settingsDialog = settingsDialog(
                self.station,
                self.station.updateValueSettings,
                self.station.updateSettingsFile,
                self.station.resetSettings,
            )

        self.stepStepDialog = StepSelectionDialog(self.station.steps)

        if station.adminPassword is not None:
            self.passwordDialog = PasswordDialog(station.adminPassword)

        self.initUI()

        self.workerThread = threading.Thread(target=self.start)
        self.workerThread.daemon = True
        self.workerThread.start()

    def initUI(self):
        self.initWidgets()
        centerWidget = QWidget()

        vlayoutMain = QVBoxLayout()
        hlayoutChild = QHBoxLayout()

        vlayoutMain.addWidget(self.runViewerWidget)
        vlayoutMain.addWidget(self.stationStatusWidget)

        self.splitter.addWidget(self.tabManagerWidget)
        self.splitter.addWidget(self.loggerWidget)

        hlayoutChild.addWidget(self.splitter)

        if self.settingsDialog is not None:
            hlayoutChild.addWidget(self.settingsViewerWidget)

        vlayoutMain.addLayout(hlayoutChild)
        if self.stationInfoWidget is not None:
            vlayoutMain.addWidget(self.stationInfoWidget)
        vlayoutMain.setStretchFactor(hlayoutChild, 60)

        centerWidget.setLayout(vlayoutMain)
        self.setCentralWidget(centerWidget)
        self.setMinimumSize(640, 480)
        self.setWindowTitle(self.station.getDisplayName())

    def initWidgets(self):
        self.loggerWidget = LoggerWidget()
        self.station.logger.addHandler(self.loggerWidget)
        self.splitter = QSplitter()
        self.tabManagerWidget = TabManagerWidget(self.station)
        self.stationStatusWidget = StationStatusWidget()
        self.runViewerWidget = RunViewerWidget(self.station)
        if self.settingsDialog is not None:
            self.settingsViewerWidget = SettingsViewerWidget(self.station)
            self.settingsDialog.accepted.connect(self.settingsViewerWidget.refresh)
        if (
            self.station.STATION_VERSION is not None
            and len(self.station.STATION_VERSION) > 0
        ):
            self.stationInfoWidget = StationInfoWidget(self.station.STATION_VERSION)
        self.updateLayoutDebug()

    def updateLayoutDebug(self):
        if self.debugDisplay:
            self.loggerWidget.show()
            if self.settingsDialog:
                self.settingsViewerWidget.show()
        else:
            self.loggerWidget.hide()
            if self.settingsDialog:
                self.settingsViewerWidget.hide()

    def start(self):
        self.station.start()

    def nextStepHandlerUI(self):
        self.tabManagerWidget.updateCurrentTab()
        self.runViewerWidget.updateCurrentTab()

    def skipStepHandlerUI(self):
        self.runViewerWidget.currentTabSkipped()

    def clearStepsHandlerUI(self):
        self.runViewerWidget.reset()
        # we re-update the current tab, it was cleaned with the previous reset
        self.runViewerWidget.updateCurrentTab()

    def stepOKHandlerUI(self):
        self.runViewerWidget.currentTabOK()

    def stepKOHandlerUI(self):
        self.runViewerWidget.currentTabKO()

    def endRunHandlerUI(self, runObj):
        self.stationStatusWidget.update(runObj)

    def forceStepHandlerUI(self, index, clearRunViewer=False):
        if clearRunViewer:
            self.runViewerWidget.reset()
        self.tabManagerWidget.switchToTabIndex(index)

    def passwordDialogWrapper(self, secondDialog):
        showDialog = True
        if self.passwordDialog:
            showDialog = self.passwordDialog.exec_() == 1
        if showDialog is True:
            secondDialog.show()

    def keyPressEvent(self, event):
        k = event.key()

        # Quit via Ctrl-Q
        if k == Qt.Key_Q and (QApplication.keyboardModifiers() & Qt.ControlModifier):
            self.close()

        # Settings via Ctrl-P
        if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_P):
            if self.settingsDialog:
                self.passwordDialogWrapper(self.settingsDialog)

        # Step selection via Ctrl-T
        if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_T):
            self.passwordDialogWrapper(self.stepStepDialog)

        # Debug layout via Ctrl-B
        if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_B):
            self.debugDisplay = not self.debugDisplay
            self.updateLayoutDebug()

    def writeWorkflow(self):
        self.station.writeWorkflow()
