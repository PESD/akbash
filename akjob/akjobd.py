""" A script to start the akjob daemon.

This script is not designed to be imported. Run from the command line or
subprocess.run.

python-daemon asks for pylockfile but that package is depreciated. Instead I'm
using pid which is python-daemon compatible.
"""

import os
import sys
import argparse
import pid
import daemon
import logging
from time import sleep


# Set up logging
logging.basicConfig()
logger = logging.getLogger("akjobd")
logger.setLevel(logging.DEBUG)

# setup piddir and pidname from command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("action",
                    choices=["start", "stop"],
                    help="Action to perform.")
parser.add_argument("-pd", "--piddir",
                    required=True,
                    help="The directory used to store the pid file.")
parser.add_argument("-pn", "--pidname",
                    required=True,
                    help="The name of the pid file.")
parser.add_argument("-ld", "--logdir",
                    help="The directory used to store the log file.")
parser.add_argument("-ln", "--logname",
                    help="The name of the log file.")
args = parser.parse_args()

piddir = args.piddir
pidfile = args.pidname


def stop_daemon(pid):
    logger.info("Stopping Daemon. Sending SIGTERM to pid " + str(pid))
    os.kill(pid, 15)  # 15 = SIGTERM - "Software termination signal"
    raise SystemExit

def start_daemon():
    logger.info("Starting the akjob daemon.")
    with daemon.DaemonContext(pidfile=pid.PidFile(pidname=pidfile, piddir=piddir)):
        while True:
            sleep(10)


# Before the daemon starts it checks the pid file but I can't monitor the
# results so here I'm doing a pre-check on the pidfile.
# logger.info("Checking PID file.")
pidcheck = pid.PidFile(pidname=pidfile, piddir=piddir)
pidstatus = None
try:
    pidstatus = pidcheck.check()
    if pidstatus:
        logger.info(pidstatus)
except pid.PidFileAlreadyRunningError as err:
    logger.info(err)
    if args.action == "stop":
        stop_daemon(pidcheck.pid)
    raise SystemExit
except:
    logger.error('Unknown pid related error: ' + str(sys.exc_info()[1:2]))
    raise SystemExit

if args.action == "stop":
    stop_daemon(pidcheck.pid)
elif args.action == "start":
    start_daemon()
else:
    logger.error("Didn't receive start or stop command.")
