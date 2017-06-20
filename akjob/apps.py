"""
Start the akjob daemon.

### pidfile location ###
I'm thinking the best location is /var/run so the pid file is delete when the
system reboots. So if there is a sudden power loss, akjobd will still start.
This will probably only be setup in production. We need the sysadmin to set up
a directory for akjob under /var/run that akbash will have write permissions
to. The directory and permissions have to be re-setup on system start since
/var/run is on a tmpfs and is recreated each system start. That means making an
init script.
OR... maybe use the /tmp dir if it's cleaned when the system starts but under
systemd that's not the case but it is cleaned periodically from a cron job.
OR... maybe place the pid file in the akjob dir then write code look at the
processes once in a while and delete the pidfile if it exists but the daemon
isn't running.

Pid file default is BASE_DIR/akjob/akjobd.pid. You can use AKJOB_PID_DIR and
AKJOB_PID_FILE enviroment variables to over ride.
"""
import os
from subprocess import run
from django.conf import settings
from django.apps import AppConfig


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
        run(["python", "akjob/akjobd.py",
             "-pd", AKJOB_PID_DIR,
             "-pn", AKJOB_PID_FILE])
