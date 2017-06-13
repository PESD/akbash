"""
Schedule and run jobs. Run as a daemon.

Consider using python-daemon (https://pagure.io/python-daemon) to create a
    deamon process.
Consider using signal to catch things such a shutdown signals.

Create job class. job objects submitted to scheduler.

scheduler Methods:
List jobs, delete jobs, add jobs.

one time jobs, recuring jobs, recuring jobs that can delete themselves when
mission accomplished.

Submit job. Pass an object containing the job code along with scheduling
options. Or submit funtion/method to be ran with needed paramaters/args.
"""

import pid
from time import sleep


def do_the_things():
    pass


def main():
    while True:
        do_the_things()
        sleep(10)


# this type of setup enables this script to be ran from cron, for instance,
# every minute and prevents a 2nd copy from being ran. In this way cron is used
# to start the daemon if it's not running. The other option is to use the
# standard OS way of starting daemons, init.d and similar or installing
# daemontools/supervise.
if __name__ == '__main__':
    with pid.PidFile('akbash_scheduler'):
        main()
        # when calling main() consider forking to a new process, possibly using
        # python-daemon in main() to daemonize the process.
