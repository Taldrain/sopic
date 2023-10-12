import datetime
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


def formatDisplayStat(x, y):
    return "{}/{} ({:.0f}%)".format(x, y, (0 if y == 0 else x / y) * 100)


class StationStatusWidget(QWidget):
    _avg_time = 0

    _nb_pass_label = None
    _nb_fail_label = None
    _nb_consecutive_fail_label = None
    _run_timer_label = None
    _station_time_label = None

    def __init__(self):
        super().__init__()

        self._init_widgets()

        layout = QHBoxLayout()

        layout.addWidget(self._nb_pass_label)
        layout.addWidget(self._nb_fail_label)
        layout.addWidget(self._nb_consecutive_fail_label)
        layout.addWidget(self._run_timer_label)
        layout.addWidget(self._station_time_label)

        self.setLayout(layout)

    def _init_widgets(self):
        self._nb_pass_label = QLabel()
        self._nb_fail_label = QLabel()
        self._nb_consecutive_fail_label = QLabel()
        self._run_timer_label = QLabel()
        self._station_time_label = QLabel(
            "Date: {}".format(datetime.date.today().isoformat())
        )

        self._update_labels(0, 0, 0, 0, 0)

    def _update_labels(
        self, nb_pass, nb_fail, nb_run, nb_consecutive_fails, time_spent
    ):
        self._nb_pass_label.setText(
            "Number of successes: " + formatDisplayStat(nb_pass, nb_run)
        )
        self._nb_fail_label.setText(
            "Number of fails: " + formatDisplayStat(nb_fail, nb_run)
        )
        self._nb_consecutive_fail_label.setText(
            "Consecutive fails: " + str(nb_consecutive_fails)
        )
        self._run_timer_label.setText(
            "Previous run: {}s (avg: {:.1f}s)".format(time_spent, self._avg_time)
        )

    def update(self, nb_fail, nb_run, start_date, nb_consecutive_fails):
        nb_pass = nb_run - nb_fail
        run_duration = (datetime.datetime.utcnow() - start_date).seconds
        time_spent = (datetime.datetime.utcnow() - start_date).seconds

        if nb_run > 0:
            self._avg_time = (
                self._avg_time * (nb_run - 1) / nb_run
            ) + run_duration / nb_run

        self._update_labels(nb_pass, nb_fail, nb_run, nb_consecutive_fails, time_spent)
