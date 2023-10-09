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

from .station_status_widget import StationStatusWidget
from .station_info_widget import StationInfoWidget
from .steps_viewer_widget import StepsViewerWidget
from .settings_dialog_widget import SettingsDialogWidget
from .logger_widget import LoggerWidget
from .start_screen_widget import StartScreenWidget


class MainWindow(QMainWindow):
    _station = None

    _splitter_widget = None
    _station_status_widget = None
    _station_info_widget = None
    _steps_viewer_widget = None
    _settings_dialog_widget = None
    _logger_widget = None
    _start_screen_widget = None

    _debug_display = False

    def __init__(self, station, start_screen_widget=StartScreenWidget):
        super().__init__()

        self._station = station(
            self.next_step_handlerUI,
            self.end_run_handlerUI,
        )

        self._init_widgets()
        self._init_ui()

        _worker_thread = threading.Thread(target=self.start)
        _worker_thread.daemon = True
        _worker_thread.start()

    def _init_widgets(self, start_screen_widget=StartScreenWidget):
        self._logger_widget = LoggerWidget()
        self._station.logger.addHandler(self._logger_widget)

        self._splitter_widget = QSplitter()
        self._station_status_widget = StationStatusWidget()

        self._steps_viewer_widget = StepsViewerWidget(self._station.get_steps())

        self._start_screen_widget = start_screen_widget()
        self._steps_viewer_widget.insert_tab(0,
                                             self._start_screen_widget,
                                             self._start_screen_widget.TAB_NAME)

        if len(self._station._settings) != 0:
            self._settings_dialog_widget = SettingsDialogWidget(
                self._station._get_settings_handler,
                self._station._reset_settings_handler,
                self._station._save_settings_handler,
            )

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

        v_layout_main.addWidget(self._station_status_widget)

        self._splitter_widget.addWidget(self._steps_viewer_widget)
        self._splitter_widget.addWidget(self._logger_widget)

        h_layout_child.addWidget(self._splitter_widget)

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
        else:
            self._logger_widget.hide()

    def start(self):
        # before starting the first run we will display the StartScreenWidget
        self.start_screen_display(True)
        self._station.start()

    def start_screen_display(self, first_run, is_success=False, fails=[]):
        self._steps_viewer_widget.setCurrentWidget(self._start_screen_widget)
        self._start_screen_widget.start(first_run, is_success, fails)


    def next_step_handlerUI(self, step):
        self._steps_viewer_widget.update_tab(step)

    def end_run_handlerUI(self,
                          nb_fail,
                          nb_run,
                          start_date,
                          nb_consecutive_fails,
                          is_success,
                          fails):
        self._station_status_widget.update(
            nb_fail, nb_run, start_date, nb_consecutive_fails
        )
        # display the StartScreenWidget as a recap of the previous run and a
        # way to start the next run
        self.start_screen_display(False, is_success, fails)

    def keyPressEvent(self, event):
        k = event.key()

        # Quit via Ctrl-Q
        if k == Qt.Key_Q and (QApplication.keyboardModifiers() & Qt.ControlModifier):
            self.close()

        # Settings via Ctrl-P
        if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_P):
            if (len(list(self._station.default_settings)) > 0):
                self._settings_dialog_widget.show()

        # Debug layout via Ctrl-B
        if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (k == Qt.Key_B):
            self._debug_display = not self._debug_display
            self._update_layout_debug()
