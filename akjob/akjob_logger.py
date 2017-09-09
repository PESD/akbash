""" Akjob logging configuration.

Typically a root logger is setup and propagation is used so the loggers in each
module use the handlers in the root logger. This is NOT how I've set this up.
Maybe I should do it that way. I'm bad at this. But all file descriptors are
closed when a deamon is detached so I need a little more flexibility for akjob.

Akjob specific for now with future plans to make this available for all Akbash
and moved into the Akbash package.
"""

import os
import logging
from django.conf import settings


class AkjobLogging():
    """ Akbash pre-configured logging objects.

    The idea is to create an AkjobLogging intance that will give you a
    pre-configured logging instance. But since you also have the AkbashLogging
    instance with all it's attributes, it's easier to adjust the config.
    """


    # default log file location
    basedir = settings.BASE_DIR
    logdir = os.path.join(basedir, "akjob", "logs")
    # default log formats
    default_format_str = (
        '%(asctime)s %(levelname)s:%(name)s:%(module)s --- %(message)s')
    multiline_format_str = ("%(asctime)s %(levelname)s:%(name)s:%(module)s" +
                            "\n    %(message)s")
    thread_format_str = ("%(asctime)s %(levelname)s:%(name)s:%(module)s:" +
                         "%(threadName)s:%(thread)s\n    %(message)s")


    def __init__(
            self,
            name="akjob",
            logfilename="akjob.log",
            logdir=logdir,
            format_str=default_format_str,
            interval=23,  # rotate log every 23 hours. (when="H" (hours))
            when="H",  # Goes with inteval. "H" for hours.
            backupCount=14,  # Log rotation. Delete old files, keep last 14.
            loglevel=None
    ):

        self.name = name
        self.logfilename = logfilename
        self.logdir = logdir
        self.logfile = None  # Full path and filename
        self.format_str = format_str
        self.interval = interval
        self.when = when
        self.backupCount = backupCount
        self.loglevel = loglevel


    def setup_log_file(self, logdir=None, logfilename=None):
        if logdir is None:
            logdir = self.logdir
        if logfilename is None:
            logfilename = self.logfilename

        self.logfile = os.path.join(logdir, logfilename)
        if not os.path.exists(logdir):
            os.makedirs(logdir)

    def setup_handlers(self):
        # log to console and rotating log files.
        self.fh = logging.handlers.TimedRotatingFileHandler(
            self.logfile,
            interval=self.interval,
            backupCount=self.backupCount
        )
        self.ch = logging.StreamHandler()

    def setup_formatter(self, format_str=None):
        if format_str is None:
            format_str = self.format_str

        self.formatter = logging.Formatter(format_str)
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)

    def setup_logger(self, name=None):
        if name is None:
            name = self.name

        # create logging intance.
        self.logger = logging.getLogger(self.name)
        self.logger.handlers = []  # remove any default handlers
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)
        # This isn't designed with propagation in mind.
        self.logger.propagate = False

        # Default loglevel of WARNING or DEBUG if django site DEBUG is turned on.
        if self.loglevel is not None:
            self.logger.setLevel(self.loglevel)
        else:
            if settings.DEBUG is True:
                self.logger.setLevel(logging.DEBUG)
            else:
                self.logger.setLevel(logging.WARNING)

    def get_logger(self=None, logdir=None, logfilename=None, format_str=None,
                   name=None):
        self.setup_log_file(logdir=logdir, logfilename=logfilename)
        self.setup_handlers()
        self.setup_formatter(format_str=format_str)
        self.setup_logger(name=name)
        self.logger.debug("Logger is setup.")
        return self.logger
