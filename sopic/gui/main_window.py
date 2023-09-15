import threading

from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
)
from PySide6.QtCore import Qt

# from PyQt5.QtWidgets import (
#     QWidget,
#     QMainWindow,
#     QHBoxLayout,
#     QVBoxLayout,
#     QApplication,
#     QSplitter,
# )
#
# from PyQt5.QtCore import Qt

# from .logger_widget import LoggerWidget
# from .tab_manager_widget import TabManagerWidget
# from .run_viewer_widget import RunViewerWidget
# from .settings_viewer_widget import SettingsViewerWidget
# from .step_selection_dialog import StepSelectionDialog
from .station_status_widget import StationStatusWidget
from .station_info_widget import StationInfoWidget
from .steps_viewer_widget import StepsViewerWidget
from .settings_dialog_widget import SettingsDialogWidget
from .logger_widget import LoggerWidget

# from .password_dialog import PasswordDialog


class MainWindow(QMainWindow):
    _station = None

    _settings_dialog = None
    _password_dialog = None

    _splitter_widget = None
    _station_status_widget = None
    _station_info_widget = None
    # _settings_viewer_widget = None
    _steps_viewer_widget = None
    _settings_dialog_widget = None
    _logger_widget = None

    # passwordDialog = None
    # splitter = None

    # loggerWidget = None
    # tabManagerWidget = None
    # stationStatusWidget = None
    runViewerWidget = None
    # settingsViewerWidget = None

    _debug_display = False

    def __init__(self, station):
        super().__init__()

        # TODO: UI handlers
        self._station = station(
            self.next_step_handlerUI,
            self.end_run_handlerUI,
        )

        # if settings_dialog is not None:
        #     self._settings_dialog = settings_dialog(
        #         self._station,
        #         self._station.updateValueSettings,
        #         self._station.updateSettingsFile,
        #         self._station.resetSettings,
        #     )

        # XXX: delete, we cannot have a disable step dialog
        # self.stepStepDialog = StepSelectionDialog(self.station.steps)

        # TODO
        # if self.station.admin_password is not None:
        #     self._password_dialog = PasswordDialog(self._station.adminPassword)

        self._init_widgets()
        self._init_ui()

        _worker_thread = threading.Thread(target=self.start)
        _worker_thread.daemon = True
        _worker_thread.start()

    def _init_widgets(self):
        # TODO: logger
        self._logger_widget = LoggerWidget()
        self._station.logger.addHandler(self._logger_widget)

        self._splitter_widget = QSplitter()
        self._station_status_widget = StationStatusWidget()

        self._steps_viewer_widget = StepsViewerWidget(self._station.get_steps())

        # XXX: rewrote to display the dag
        # self.runViewerWidget = RunViewerWidget(self.station)

        if len(self._station._settings) != 0:
            self._settings_dialog_widget = SettingsDialogWidget(
                self._station._get_settings_handler,
                self._station._reset_settings_handler,
                self._station._save_settings_handler,
            )

        # if self._settings_dialog is not None:
        # self._settings_viewer_widget = SettingsViewerWidget(self._station._settings)
        # TODO: send the settings
        # self._settings_dialog.accepted.connect(self._settings_viewer_widget.refresh)

        if (
            self._station.STATION_VERSION is not None
            and len(self._station.STATION_VERSION) > 0
        ):
            self._station_info_widget = StationInfoWidget(self._station.STATION_VERSION)

        self._update_layout_debug()

    def _init_ui(self):
        center_widget = QWidget()

        v_layout_main = QVBoxLayout()
        h_layout_child = QHBoxLayout()

        # v_layout_main.addWidget(self.runViewerWidget)
        v_layout_main.addWidget(self._station_status_widget)

        self._splitter_widget.addWidget(self._steps_viewer_widget)
        self._splitter_widget.addWidget(self._logger_widget)

        h_layout_child.addWidget(self._splitter_widget)

        if self._settings_dialog is not None:
            h_layout_child.addWidget(self.settingsViewerWidget)

        v_layout_main.addLayout(h_layout_child)
        if self._station_info_widget is not None:
            v_layout_main.addWidget(self._station_info_widget)
        v_layout_main.setStretchFactor(h_layout_child, 60)

        center_widget.setLayout(v_layout_main)
        self.setCentralWidget(center_widget)
        self.setMinimumSize(640, 480)
        self.setWindowTitle(self._station.STATION_NAME)

    def _update_layout_debug(self):
        if self._debug_display:
            self._logger_widget.show()
            # if self._settings_dialog is not None:
            #     self._settings_viewer_widget.show()
        else:
            self._logger_widget.hide()
        #     if self._settings_dialog is not None:
        #         self._settings_viewer_widget.hide()

    def start(self):
        self._station.start()

    def next_step_handlerUI(self, step):
        self._steps_viewer_widget.update_tab(step)

    # def nextStepHandlerUI(self):
    #     self.tabManagerWidget.updateCurrentTab()
    #     self.runViewerWidget.updateCurrentTab()

    # def skipStepHandlerUI(self):
    #     self.runViewerWidget.currentTabSkipped()

    # def clearStepsHandlerUI(self):
    #     self.runViewerWidget.reset()
    #     # we re-update the current tab, it was cleaned with the previous reset
    #     self.runViewerWidget.updateCurrentTab()

    # def stepOKHandlerUI(self):
    #     self.runViewerWidget.currentTabOK()
    #
    # def stepKOHandlerUI(self):
    #     self.runViewerWidget.currentTabKO()

    def end_run_handlerUI(self, nb_fail, nb_run, start_date, nb_consecutive_fails):
        self._station_status_widget.update(
            nb_fail, nb_run, start_date, nb_consecutive_fails
        )

    def forceStepHandlerUI(self, index, clearRunViewer=False):
        if clearRunViewer:
            self.runViewerWidget.reset()
        self.tabManagerWidget.switchToTabIndex(index)

    def passwordDialogWrapper(self, secondDialog):
        showDialog = True
        # TODO
        # if self.passwordDialog:
        #     showDialog = self.passwordDialog.exec_() == 1
        if showDialog is True:
            secondDialog.show()

    def keyPressEvent(self, event):
        k = event.key()

        # Quit via Ctrl-Q
        if k == Qt.Key_Q and (QApplication.keyboardModifiers() & Qt.ControlModifier):
            self.close()

        # Settings via Ctrl-P
        if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_P):
            if self._settings_dialog_widget:
                self.passwordDialogWrapper(self._settings_dialog_widget)

        # # Step selection via Ctrl-T
        # if (QApplication.keyboardModifiers() & Qt.ControlModifier)
        #   and (k == Qt.Key_T):
        #     self.passwordDialogWrapper(self.stepStepDialog)

        # Debug layout via Ctrl-B
        if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_B):
            self._debug_display = not self._debug_display
            self._update_layout_debug()
