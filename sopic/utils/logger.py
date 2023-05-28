import os
import logging
import colorlog

DEFAULT_LEVEL = logging.DEBUG
FORMAT = "[%(levelname)s] %(asctime)s | %(name)s | %(message)s"
WIDGET_FORMAT = "%(asctime)s | %(name)s | %(message)s"


class WidgetFormatter(logging.Formatter):
    def format(self, record):
        if "." in record.name:
            parent_name, child_name = record.name.rsplit(".", 1)
            record.name = f"{parent_name} -> {child_name}"
        return super().format(record)


def _default_formatter():
    return logging.Formatter(FORMAT)


def _colored_formatter():
    return colorlog.ColoredFormatter(f"%(log_color)s{FORMAT}")


def widget_formatter():
    return WidgetFormatter(fmt=WIDGET_FORMAT, datefmt="%H:%M:%S")


def _station_logger_name(name, id):
    return f"{id:03}-{name}"


def init_station_logger(station_name, station_id, log_dir, disable_file_logging):
    logger_name = _station_logger_name(station_name, station_id)
    logger = logging.getLogger(logger_name)
    logger.setLevel(DEFAULT_LEVEL)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(DEFAULT_LEVEL)
    console_handler.setFormatter(_colored_formatter())
    logger.addHandler(console_handler)

    # file handler
    if disable_file_logging is False:
        directory = os.path.expanduser(log_dir)
        os.makedirs(directory, exist_ok=True)
        file_handler = logging.FileHandler(
            os.path.join(directory, f"{logger_name}.log")
        )
        file_handler.setLevel(DEFAULT_LEVEL)
        file_handler.setFormatter(_default_formatter())
        logger.addHandler(file_handler)

    return logger


def get_step_logger(station_name, station_id, step_name):
    logger_name = f"{_station_logger_name(station_name, station_id)}.{step_name}"
    return logging.getLogger(logger_name)
