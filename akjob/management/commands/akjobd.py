from django.core.management.base import BaseCommand, CommandError
from akjob import akjobd
from akjob import models

class Command(BaseCommand):
    help = ("This akjobd control utility allows you to start, stop, and " +
            "restart akjobd.")

    def add_arguments(self, parser):
        parser.add_argument("action",
                            choices=["start", "stop", "restart",
                                     "reloadfixture", "joblist", "enablejob",
                                     "disablejob", "deletejob", "showinfo"],
                            help="""
Action to perform.

Start, stop, or restart the akjobd daemon.

reloadfixture will remove objects from DayOfMonth, DayOfWeek, and Months tables
then reload them.

joblist will display a list of all jobs.

enablejob, disablejob, deletejob will enable, disble, or delete the job
specified by -id.

showinfo will display information about the job specified by -id.
""")
        parser.add_argument("-pd", "--piddir",
                            help="The directory used to store the pid file. "
                                 "Optional. Defaults to BASE_DIR/akjob/")
        parser.add_argument("-pn", "--pidname",
                            help='The name of the pid file. Optional. Defaults'
                                 ' to "akjobd.pid"')
        parser.add_argument("-id",
                            help='ID number of job to enable, disable, '
                                 'delete or showinfo')


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
            models.load_DayOfMonth(refresh=True)
            models.load_DayOfWeek(refresh=True)
            models.load_Months(refresh=True)
        elif options["action"] == "joblist":
            models.list_jobs()
        elif options["action"] in ["enablejob", "disablejob", "deletejob",
                                   "showinfo"]:
            if options["id"] is None:
                raise CommandError(
                    'Job id is required with action "' +
                    options["action"] + '".')
            try:
                if not models.job_exists(int(options["id"])):
                    raise CommandError("Job " + options["id"] + " doesn't exist.")
            except ValueError:
                raise CommandError("The id supplied is not an integer.")
            if options["action"] == "enablejob":
                models.enable_job(int(options["id"]))
            elif options["action"] == "disablejob":
                models.disable_job(int(options["id"]))
            elif options["action"] == "deletejob":
                models.delete_job(int(options["id"]))
            elif options["action"] == "showinfo":
                models.Job.objects.get(id=int(options["id"])).print()
