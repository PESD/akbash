"""
python-daemon asks for pylockfile but that package is depreciated. Instead I'm
using pid which is python-daemon compatible.

Do I need to define what to do in response to diferent signals or is the
default that python-daemon uses good enough?

Start the daemon using AppConfig.ready()
"""

import pid
import daemon
import logging
from time import sleep


# It's best to setup a directory under /var/run for the lockfile but will
# probably only do that in production and we need the sysadmin to set that up.
# Or... maybe write code look at the processes once in a while and delete the
# pidfile if it exists but the daemon isn't running.
pidfile = "akjobd.pid"
piddir = "/Users/robwirk/dev/akbash/"

# Let's check the lockfile before daemonizing or else we won't see the error
# messages.
"""
try:
    with pid.PidFile(pidname=pidfile, piddir=piddir):
        pass
except:
    print("Something went wrong when checking the pid file/lock file")
    raise
"""

# It's actually better for it to fail quietly. Instead use logger to log a
# notice.
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    with pid.PidFile(pidname=pidfile, piddir=piddir):
        pass
except pid.PidFileAlreadyLockedError as err:
    logger.info("pid.PidFileAlreadyLockedError. The daemon is probably already running.")
    raise SystemExit
except:
    logger.info('pid stuff error')
    raise SystemExit


# Start the daemon
with daemon.DaemonContext(pidfile=pid.PidFile(pidname=pidfile, piddir=piddir)):
    while True:
        sleep(10)
