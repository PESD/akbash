"""
Start the akjob daemon when akbash starts up

Set enviroment variable AKJOB_START_DAEMON to false if you don't want the
daemon started on akbash startup.

Pid file default is BASE_DIR/akjob/akjobd.pid. You can use AKJOB_PID_DIR and
AKJOB_PID_FILE enviroment variables to over ride.

This script is assuming that akbash is started from the BASE_DIR. Hopefully
that's an okay assumption.
"""
import sys
import os
from subprocess import run
from django.conf import settings
from django.apps import AppConfig


BASE_DIR = settings.BASE_DIR

AKJOB_START_DAEMON = os.environ.get(
    "AKJOB_START_DAEMON", True)

AKJOB_PID_DIR = os.environ.get(
    "AKJOB_PID_DIR",
    os.path.join(BASE_DIR, "akjob"))

AKJOB_PID_FILE = os.environ.get(
    "AKJOB_PID_FILE",
    "akjobd.pid")

AKJOB_LOG_DIR = os.environ.get(
    "AKJOB_LOG_DIR",
    os.path.join(BASE_DIR, "akjob", "logs"))

AKJOB_PYTHON = os.environ.get("AKJOB_PYTHON",
                              os.path.join(sys.prefix, "bin", "python"))

AKJOB_UNITTEST = os.environ.get("AKJOB_UNITTEST", False)


class AkjobConfig(AppConfig):
    name = "akjob"

    def ready(self):
        "Start the akjob daemon when akbash starts up."
        if AKJOB_START_DAEMON in [True, 'True', 'true', 'TRUE', 't', 'T', 'y',
                                  'Y', 'Yes', 'yes', 'YES', '1', 1]:
            # Run akjobd.py from the BASE_DIR instead of from the akjob dir.
            os.chdir(BASE_DIR)

            # start akjobd using it's own process and instance of python so
            # that it will detach when it daemonizes and this process may
            # continue on as normal and uneffected.
            command = [AKJOB_PYTHON, "akjob/akjobd.py",
                       "start",
                       "-pd", AKJOB_PID_DIR,
                       "-pn", AKJOB_PID_FILE,
                       "-ld", AKJOB_LOG_DIR,
                       "-bd", BASE_DIR,
                       ]
            if AKJOB_UNITTEST in [True, 'True', 'true', 'TRUE', 't', 'T', 'y',
                                  'Y', 'Yes', 'yes', 'YES', '1', 1]:
                command.append("-t")
            run(command)
            os.environ['AKJOB_START_DAEMON'] = 'False'
