""" Akjob Logger. """

import os
import logging
from django.conf import settings


# default log file location
basedir = settings.BASE_DIR
logdir = basedir + "/akjob/logs"


def get_logger(
        logdir=logdir,
        logname="akjob.log",
        name="akjob",
        backupCount=14,  # For log rotation. Delete old files, keep 14.
):
    """ Return an akjob pre-configured logging instance. """

    # Sort out the log file location.
    logfile = os.path.join(logdir, logname)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    logger = logging.getLogger("akjob")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s:%(name)s --- %(message)s' +
        ' --- %(module)s:%(threadName)s:%(thread)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.debug("Logger is setup.")
