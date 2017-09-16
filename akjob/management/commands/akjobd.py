from django.core.management.base import BaseCommand  # , CommandError
from akjob import akjobd
from akjob.models import DayOfMonth, DayOfWeek, Months
from akjob.models import load_DayOfMonth, load_DayOfWeek, load_Months


class Command(BaseCommand):
    help = ("This akjobd control utility allows you to start, stop, and " +
            "restart akjobd.")

    def add_arguments(self, parser):
        parser.add_argument("action",
                            choices=["start", "stop", "restart",
                                     "reloadfixture"],
                            help="Action to perform.")
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
            from akjob.akjob_logger import AkjobLogging
            akjob_logging = AkjobLogging(
                name="akjob.management", logfilename="akjobd.log")
            logger = akjob_logging.get_logger()

            # TODO: Transactions should be used to avoid race conditions.
            #       The people running this command should know what they're
            #       doing so I'm not that concerned about it. actually those
            #       functions in akjob.models should probably be made better to
            #       handle all that.
            logger.info("Reloading DayOfMonth")
            DayOfMonth.objects.all().delete()
            load_DayOfMonth()

            logger.info("Reloading DayOfWeek")
            DayOfWeek.objects.all().delete()
            load_DayOfWeek()

            logger.info("Reloading Months")
            Months.objects.all().delete()
            load_Months()
