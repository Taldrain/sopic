import os
import logging
import colorlog

DEFAULT_LEVEL = logging.DEBUG

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def getDefaultFormatter():
    return logging.Formatter(FORMAT)

def getColorFormatter():
    return colorlog.ColoredFormatter('%(log_color)s' + FORMAT)

def getLogger(name, id, disable_file_logging, default_dir, other_handlers, disable_handlers):
    logger = logging.getLogger(name + '[' + str(id) + ']')
    logger.setLevel(DEFAULT_LEVEL)

    # if the logger has already been created we don't re-add the handlers
    if (len(logger.handlers) != 0 or disable_handlers):
        return logger

    # handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(DEFAULT_LEVEL)

    if (disable_file_logging is False):
        directory = os.path.expanduser(default_dir)
        os.makedirs(directory, exist_ok=True)
        fileHandler = logging.FileHandler(os.path.join(
            directory,
            ("%03d" % id) + '-' + name + '.log',
        ))
        fileHandler.setLevel(DEFAULT_LEVEL)

    # add formatter to handler
    consoleHandler.setFormatter(getColorFormatter())
    if (disable_file_logging is False):
        fileHandler.setFormatter(getDefaultFormatter())

    # add handler to logger
    logger.addHandler(consoleHandler)
    if (disable_file_logging is False):
        logger.addHandler(fileHandler)

    for handler in other_handlers:
        logger.addHandler(handler)

    return logger
