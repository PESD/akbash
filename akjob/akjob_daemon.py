"""
python-daemon asks for pylockfile but that package is depreciated. Instead I'm
using pid which is python-daemon compatible.

Do I need to define what to do in response to diferent signals or is the
default that python-daemon uses good enough?

Start the daemon using AppConfig.ready()
"""

import daemon
import pid
from time import sleep


# def do_the_things():
#     pass


# def start_daemon():
with daemon.DaemonContext(pidfile=pid.PidFile('/Users/robwirk/dev/akbash/akjob.pid')):
    # with daemon.DaemonContext(): # This works. The above with pidfile doesn't
    # work.
    while True:
        # do_the_things()
        sleep(6)


# Enable to daemon to be started from the command line.
# if __name__ == '__main__':
#     start_daemon()
