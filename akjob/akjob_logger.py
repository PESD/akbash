""" Akjob logging configuration. """

import os
import logging
from django.conf import settings


# default log file location
basedir = settings.BASE_DIR
logdir = os.path.join(basedir, "akjob", "logs")


def get_logger(
        logdir=logdir,
        logname="akjob.log",
        name="akjob",
        interval=23,  # rotate log every 23 hours. (when="H" (hours))
        when="H",  # Goes with inteval. "H" for hours.
        backupCount=14,  # Log rotation. Delete old files, keep last 14.
        loglevel=None
):
    """ Return an akjob pre-configured logging instance. """

    # Sort out the log file location.
    logfile = os.path.join(logdir, logname)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    # log to console and rotating log files. Set formatting.
    fh = logging.handlers.TimedRotatingFileHandler(
        logfile,
        interval=interval,
        backupCount=backupCount
    )
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s:%(name)s --- %(message)s' +
        ' --- %(module)s:%(threadName)s:%(thread)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # create logging intance.
    logger = logging.getLogger(name)
    logger.handlers = []  # remove any default handlers
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.propagate = False  # This isn't designed with propagation in mind.

    # Default loglevel of WARNING or DEBUG if django site DEBUG is turned on.
    if loglevel is not None:
        logger.setLevel(loglevel)
    else:
        if settings.DEBUG is True:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)

    logger.debug("Logger is setup.")

    return logger
