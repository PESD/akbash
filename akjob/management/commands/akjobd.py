import os
from django.core.management.base import BaseCommand  # , CommandError
from django.conf import settings as django_settings
from akjob import akjobd
# from akjob.akjobd import stop_daemon, start_daemon, pid_precheck
# from akjob.akjobd import get_pid_from_pidfile


class Command(BaseCommand):
    help = ("This akjobd control utility allows you to start, stop, and " +
            "restart akjobd.")

    def add_arguments(self, parser):
        parser.add_argument("action",
                            choices=["start", "stop", "restart"],
                            help="Action to perform.")
        parser.add_argument("-pd", "--piddir",
                            help="The directory used to store the pid file. "
                                 "Optional. Defaults to BASE_DIR/akjob/")
        parser.add_argument("-pn", "--pidname",
                            help='The name of the pid file. Optional. Defaults'
                                 ' to "akjobd.pid"')


    def handle(self, *args, **options):

        if options["piddir"] is not None:
            piddir = options["piddir"]
        else:
            piddir = os.path.join(django_settings.BASE_DIR, "akjob")

        if options["pidname"] is not None:
            pidname = options["pidname"]
        else:
            pidname = "akjobd.pid"

        pidfile_location = os.path.abspath(os.path.join(piddir, pidname))

        # This is not working. I wanted to confirm the existance of the pid
        # file. really this stuff needs to be restructered now that the
        # infinate loop problems is fixed. Rethink how akjobd is started. Look
        # at apps.py, akjobd.py, and this file.
        akjobd.piddir = piddir
        akjobd.pidfile = pidname
        pid = akjobd.get_pid_from_pidfile(piddir, pidname)

        self.stdout.write("PID: " + str(pid))
        self.stdout.write("pid file location: " + pidfile_location)
