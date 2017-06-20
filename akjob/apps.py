"""
Start the akjob daemon when akbash starts up

Set enviroment variable AKJOB_START_DAEMON to false if you don't want the
daemon started on akbash startup.

Pid file default is BASE_DIR/akjob/akjobd.pid. You can use AKJOB_PID_DIR and
AKJOB_PID_FILE enviroment variables to over ride.

This script is assuming that akbash is started from the BASE_DIR. Hopefully
that's an okay assumption.
"""
import os
from subprocess import run
from django.conf import settings
from django.apps import AppConfig


AKJOB_START_DAEMON = os.environ.get(
    "AKJOB_START_DAEMON", True)

AKJOB_PID_DIR = os.environ.get(
    "AKJOB_PID_DIR",
    os.path.join(settings.BASE_DIR, "akjob"))

AKJOB_PID_FILE = os.environ.get(
    "AKJOB_PID_FILE",
    "akjobd.pid")


class AkjobConfig(AppConfig):
    name = "akjob"

    def ready(self):
        "Start the akjob daemon when akbash starts up."
        if AKJOB_START_DAEMON in ['True', 'true', '1', 't', 'T', 'y', 'Yes',
                                  'YES', 1, True]:
            run(["python", "akjob/akjobd.py",
                "start",
                 "-pd", AKJOB_PID_DIR,
                 "-pn", AKJOB_PID_FILE])
