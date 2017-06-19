""" A script to start the akjob daemon.

This script is not designed to be imported.

python-daemon asks for pylockfile but that package is depreciated. Instead I'm
using pid which is python-daemon compatible.
"""

import os
import sys
import pid
import daemon
import logging
from time import sleep
from django.conf import settings


# pidfile location
# It's best to setup a directory under /var/run for the lockfile but will
# probably only do that in production and we need the sysadmin to set that up.
# Probably need an init script that creates the akjob dir under /var/run and
# set permissions so akjob can write to it.
# Or... maybe use the /tmp dir if it's cleaned when the system starts.
# Or... maybe write code look at the processes once in a while and delete the
# pidfile if it exists but the daemon isn't running.
sys.path.insert(1, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akbash.settings")
piddir = settings.BASE_DIR
pidfile = "akjobd.pid"

# Set up logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Before the daemon starts it checks the pid file but I can't monitor the
# results so here I'm doing a pre-check on the pidfile.
"""
logger.info("Attempting to start the akjob daemon.")
try:
    with pid.PidFile(pidname=pidfile, piddir=piddir):
        pass
except pid.PidFileAlreadyLockedError as err:
    logger.info("pid.PidFileAlreadyLockedError. The daemon is probably already running.")
    raise SystemExit
except:
    logger.info('pid stuff error')
    raise SystemExit
"""
pidcheck = pid.PidFile(pidname=pidfile, piddir=piddir)
pidcheck.check()


# Start the daemon
with daemon.DaemonContext(pidfile=pid.PidFile(pidname=pidfile, piddir=piddir)):
    while True:
        sleep(10)
