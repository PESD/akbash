from django.core.management.base import BaseCommand  # , CommandError
from akjob import akjobd
from akjob.models import load_DayOfMonth, load_DayOfWeek, load_Months


class Command(BaseCommand):
    help = ("This akjobd control utility allows you to start, stop, and " +
            "restart akjobd.")

    def add_arguments(self, parser):
        parser.add_argument("action",
                            choices=["start", "stop", "restart",
                                     "reloadfixture"],
                            help="Action to perform. Start, stop, or restart "
                                 "the akjobd daemon. reloadfixture will "
                                 "remove objects from DayOfMonth, DayOfWeek, "
                                 "and Months tables then reload them.")
        parser.add_argument("-pd", "--piddir",
                            help="The directory used to store the pid file. "
                                 "Optional. Defaults to BASE_DIR/akjob/")
        parser.add_argument("-pn", "--pidname",
                            help='The name of the pid file. Optional. Defaults'
                                 ' to "akjobd.pid"')


    def handle(self, *args, **options):

        if options["piddir"] is not None:
            akjobd.piddir = options["piddir"]

        if options["pidname"] is not None:
            akjobd.pidfile = options["pidname"]

        if options["action"] == "start":
            akjobd.do_action("start")
        elif options["action"] == "stop":
            akjobd.do_action("stop")
        elif options["action"] == "restart":
            akjobd.do_action("restart")
        elif options["action"] == "reloadfixture":
            load_DayOfMonth(refresh=True)
            load_DayOfWeek(refresh=True)
            load_Months(refresh=True)
