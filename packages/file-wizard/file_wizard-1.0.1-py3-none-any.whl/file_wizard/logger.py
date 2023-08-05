"""The logger module contains the configurations for the global

"""
import logging
from typing import Any


def isHandlerPresent(log: logging.Logger, handlerClass: Any) -> bool:
    """Returns whether handler of a given class is present or not

    Args:
        log (logging.Logger):
        handlerClass (any valid handler class):
    Returns:
        bool:
    """
    for handler in log.handlers:
        if isinstance(handler, handlerClass) is True:
            return True
    return False


def removeHandler(log: logging.Logger, myHandler) -> None:
    """Removes a given handler type from the log

    Args:
        log (logging.Logger)
        myHandler (Any handler class that can be attached to log.)
    """
    for handler in log.handlers:
        if isinstance(handler, myHandler) is True:
            log.removeHandler(handler)


def addDefaultFileHandler(log: logging.Logger) -> None:
    """ Adds the default file handler

    Args:
        log (logging.Logger)
    """
    logFormatter: logging.Formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-7.7s]  %(message)s")
    fileHandler: logging.FileHandler = logging.FileHandler("debug.log",
                                                           mode="a")
    fileHandler.setFormatter(logFormatter)
    log.addHandler(fileHandler)


def addDefaultConsoleHandler(log: logging.Logger) -> None:
    """Adds the default console handler to log

    Args:
        log (logging.Logger)
    """
    consoleFormatter: logging.Formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-7.7s]  %(message)s")
    consoleHandler: logging.StreamHandler = logging.StreamHandler()
    consoleHandler.setFormatter(consoleFormatter)
    # consoleHandler.setLevel(logging.DEBUG)
    log.addHandler(consoleHandler)


def setDefaultLevel(log: logging.Logger) -> None:
    """Sets default logging level.

    Args:
        log (logging.Logger)
    """
    log.setLevel(logging.DEBUG)


def initLogger(verbose: bool = True,
               logfile: bool = True,
               defaultLevel: bool = True) -> logging.Logger:
    """Creates the log instance, if not present.

    Args:
        verbose (bool, optional):  Defaults to True.
        logfile (bool, optional):  Defaults to True.
        defaultLevel (bool, optional):  Defaults to True.

    Returns:
        logging.Logger
    """
    log: logging.Logger = logging.getLogger("FileWizard")
    if verbose is True and \
       isHandlerPresent(log, logging.StreamHandler) is False:
        addDefaultConsoleHandler(log)
    elif verbose is False:
        removeHandler(log, logging.StreamHandler)
    if logfile is True and \
       isHandlerPresent(log, logging.FileHandler) is False:
        addDefaultFileHandler(log)
    elif logfile is False:
        removeHandler(log, logging.FileHandler)
    if isHandlerPresent(log, logging.NullHandler) is False:
        nullHandler: logging.NullHandler = logging.NullHandler()
        log.addHandler(nullHandler)
    if defaultLevel is True:
        setDefaultLevel(log)
    log.setLevel(logging.DEBUG)
    return log
