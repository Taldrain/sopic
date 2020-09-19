import os
import logging
import colorlog

DEFAULT_LEVEL = logging.DEBUG

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def getDefaultFormatter():
    return logging.Formatter(FORMAT)


def getColorFormatter():
    return colorlog.ColoredFormatter("%(log_color)s" + FORMAT)


def getLogger(
    name, stationId, disableFileLogging, defaultDir, otherHandlers, disableHandlers
):
    logger = logging.getLogger(name + "[" + str(stationId) + "]")
    logger.setLevel(DEFAULT_LEVEL)

    # if the logger has already been created we don't re-add the handlers
    if len(logger.handlers) != 0 or disableHandlers:
        return logger

    # handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(DEFAULT_LEVEL)

    if disableFileLogging is False:
        directory = os.path.expanduser(defaultDir)
        os.makedirs(directory, exist_ok=True)
        fileHandler = logging.FileHandler(
            os.path.join(
                directory,
                ("%03d" % stationId) + "-" + name + ".log",
            )
        )
        fileHandler.setLevel(DEFAULT_LEVEL)

    # add formatter to handler
    consoleHandler.setFormatter(getColorFormatter())
    if disableFileLogging is False:
        fileHandler.setFormatter(getDefaultFormatter())

    # add handler to logger
    logger.addHandler(consoleHandler)
    if disableFileLogging is False:
        logger.addHandler(fileHandler)

    for handler in otherHandlers:
        logger.addHandler(handler)

    return logger
