""" The akjob daemon. """

import os
import sys
import argparse
import pid
import daemon
from datetime import datetime
from time import sleep
# from contextlib import redirect_stderr, redirect_stdout


# For debug
# import inspect
# print("akjobd module inspect:")
# print(inspect.stack())
# print("AKJOB_START_DAEMON = " + os.environ['AKJOB_START_DAEMON'])


""" Notes:
python-daemon asks for pylockfile but that package is depreciated. Instead I'm
using pid which is python-daemon compatible.

This module does not work from the command line although it's almost there. I
think maybe I need to import django into the global namespace from
setup_django(). Also something is going wrong when importing from akjob_logger.
I'm going to leave it alone for now and use the management command instead.

Bugs:
I don't understand why the job loop doesn't always run when the akjobd daemon
starts up. It works but it would be nice for it to run right away so unit
testing could be easier and quicker but also the user can see their new job
updated and scheduled right away. If the job loop does run right away,
sometimes it doesn't do anything like schedule jobs. Again don't understand
why.

Ideas for future versions:
*   Would using signals to control things be helpful?
*   Is there someway better to track if a job is running or not. If things stop
    while a job is running, the _job_running flag doesn't get turned off and
    the job will no longer run.
*   Look into catching termination signals and how they could be used to end the
    loop in a better way.
*   Query jobs that probably need to be deleted. Jobs with scheduled dates in
    the past or any job that won't run anymore. Maybe make function or
    something to delete them.


Unittest testing database:
When the akjob daemon is ran in it's own process, we need to handle switching
to the testing db when running unit tests. Default testmode to false.
Set testmode to True if running unittest so the right database is used.  It's
assumed test db is named "test_" + default db so this will fail if that default
isn't used.

Using test mode running akjob from the command line or when spawned in it own
process through subprocess.run:
  The arguments -t or --testdb are used. args.testdb is set to True.
  In setup_django(), is_test_mode() returns True.
    switch_to_unittest_db() is ran.
"""


# Check if running as root.
def check_for_root():
    if os.geteuid() == 0:
        logger.warn("akjobd running as root user.")


# setup piddir and pidname from command line arguments.
def parse_args():
    global args
    parser = argparse.ArgumentParser(description="The Akjob Daemon")
    parser.add_argument("action",
                        choices=["start", "stop", "restart"],
                        help="Action to perform.")
    parser.add_argument("-pd", "--piddir",
                        help="The directory used to store the pid file.")
    parser.add_argument("-pn", "--pidname",
                        help="The name of the pid file.")
    parser.add_argument("-ld", "--logdir",
                        help="The directory used to store the log file.")
    parser.add_argument("-bd", "--basedir",
                        help="The base directory of the akbash django site.")
    parser.add_argument("-t", "--testdb", action='store_true',
                        help="Use the unittest test database.")
    args = parser.parse_args()


def set_pre_setup_base_dir():
    # If basedir not specifid look for akbash/setting.py then use that akbash
    # directory as base dir.

    global pre_setup_base_dir

    def get_base_dir():
        # a lot of assumptions are being made here which is bad. It's best to
        # pass in the base dir so it doesn't get to this.
        if os.path.isfile("akbash/settings.py") is True:
            # We're already in the base dir. most common scenario.
            return os.path.abspath(".")
        elif os.path.isfile("../akbash/settings.py") is True:
            # We're probably in the akjob dir. 2nd most common scenario.
            return os.path.abspath("..")
        else:
            # don't know where we are but let's not search farther then "..".
            # This only returns the 1st result and that could be bad.
            for root, dirs, files in os.walk(".."):
                if os.path.basename(root) == "akbash":
                    if "settings.py" in files:
                        return os.path.abspath(root)

    try:
        if args.basedir is None:
            pre_setup_base_dir = get_base_dir()
        else:
            pre_setup_base_dir = args.basedir
    except NameError:
        pre_setup_base_dir = get_base_dir()


# Django has to be setup separately to disable the running of akjobd on django
# startup thereby causing an infinite loop.
def setup_django():

    # Set akjob to not auto start to avoid an infinate loop.
    os.environ['AKJOB_START_DAEMON'] = 'False'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akbash.settings")

    global django, F, Q  # not sure if django in global is needed.
    import django
    from django.db.models import F, Q

    if __name__ == '__main__':
        # make sure the BASE_DIR is in sys.path so the akbash.settings module
        # and the app packages can be found by django.setup().
        set_pre_setup_base_dir()
        if pre_setup_base_dir not in sys.path:
            sys.path.insert(0, pre_setup_base_dir)
        # switch to unittest test db if -t/--testdb args.
        if args.testdb is True:
            db = django.conf.settings.DATABASES["default"]["NAME"]
            django.conf.settings.DATABASES["default"]["NAME"] = 'test_' + db
            django.db.connections.close_all()
            # django.db.close_old_connections()
            os.environ['AKJOB_UNITTEST'] = 'True'
        django.setup()


    # For debug
    # print("setup_dkango Using database: " +
    #       django.conf.settings.DATABASES["default"]["NAME"])
    # print("Using database: " +
    #       django.conf.settings.DATABASES["default"]["NAME"] +
    #       " | called by: " + inspect.stack()[1][3] +
    #       " in " + inspect.stack()[1][1])

    global BASE_DIR
    BASE_DIR = django.conf.settings.BASE_DIR
    # print(BASE_DIR)  # for debug
    # os.chdir(BASE_DIR)
    global Job
    global job_log_stream
    from akjob.models import Job, models_logging
    job_log_stream = models_logging.fh.stream
    global loglevel
    if django.conf.settings.DEBUG is True:
        loglevel = 10  # 10 = DEBUG
    else:
        loglevel = 30  # 30 = WARNING


# set the pid file name and location. defaults are used if name and location
# not provided.
def set_pid_file_name():
    global pidfile

    try:
        if pidfile is None:
            pidfile = "akjobd.pid"
    except NameError:
        pidfile = "akjobd.pid"

    try:
        if args.pidname is not None:
            pidfile = args.pidname
    except NameError:
        pass


def set_pid_location():
    global piddir

    try:
        if piddir is None:
            piddir = os.path.join(BASE_DIR, "akjob")
    except NameError:
        piddir = os.path.join(BASE_DIR, "akjob")

    try:
        if args.piddir is not None:
            piddir = args.piddir
    except NameError:
        pass


def set_log_location():
    global logdir

    # Make sure logdir is defined. If not defined, set it to default. This is
    # done because the akjobd management command may have set the logdir var.
    try:
        if logdir is None:
            logdir = os.path.join(BASE_DIR, "akjob", "logs")
    except NameError:
        logdir = os.path.join(BASE_DIR, "akjob", "logs")

    # If logdir argument was given, set logdir, overriding anything else.
    try:
        if args.logdir is not None:
            logdir = args.logdir
    except NameError:
        pass  # args.logdir not defined. Do nothing.


# Set up logging
def setup_logging():
    # TODO: This is working but the logging doc says don't write to the same
    #       file from multiple processes so I should bring back using a file
    #       when not daemonized and another file for inside the daemon.
    #
    # django needs to be setup before importing akjob_logger. (this is ghetto)
    set_log_location()
    # try:
    #     from akjob_logger import AkjobLogging
    # except ModuleNotFoundError:  # noqa  My pyflake doesn't have this builtin.
    from akjob.akjob_logger import AkjobLogging

    global akjob_logging, logger
    akjob_logging = AkjobLogging(name="akjob.akjobd",
                                 logfilename="akjobd.log",
                                 logdir=logdir, loglevel=loglevel)
    logger = akjob_logging.get_logger()

# A different logger to run inside the daemon process.
# def get_daemon_logger():
#     akjob_logging = AkjobLogging(  # noqa
#         name="akjob.akjobd.daemon",
#         logfilename="akjobd.daemon.log",
#     )
#     return akjob_logging.get_logger()


def worker(idnum):
    job = Job.objects.get(id=idnum)
    dlog.info("Checking job " + str(job.id) + ", " + job.name)
    try:
        job.run()
    except Exception as inst:
        dlog.error("Something went wrong with Job " + str(job.id) + ", " +
                   job.name + "\n    " + str(inst))


def loop_through_jobs():
    "Loop through the jobs in the database and perform actions."

    # # print debugging message to stdout -> akjobd.out.
    # def debugRunCountMsg(j):
    #     print("--DEBUG ", str(j.id), "--> _run_count: ", j._run_count,
    #           " / limit: ", j.run_count_limit, " / delete on limit: ",
    #           j.delete_on_run_count_limit)

    # Delete Jobs with the deleteme flag set to True.
    for j in Job.objects.filter(deleteme=True):
        dlog.info("Deleting job " + str(j.id) + ", " + j.name)
        j.delete()

    # Deal with jobs with run count limits. If limit is reached set _next_run
    # to None. Delete Jobs set to be deleted when run count limit is reached.
    for j in Job.objects.filter(_run_count__gte=F('run_count_limit')):
        # debugRunCountMsg(j)
        if j.delete_on_run_count_limit is True:
            dlog.info("Run count limit reached. Deleting job " +
                      str(j.id) + ", " + j.name)
            j.delete()
        elif j._next_run is not None:
            dlog.debug("Run count limit reached. Setting _next_run to None on"
                       " job " + str(j.id) + ", " + j.name)
            j._next_run = None
            j.save()
        else:
            dlog.info("Run count limit reached. Job " +
                      str(j.id) + ", " + j.name)

    # If job is disabled but _next_run is not None, set to _next_run to None.
    for j in Job.objects.filter(
            job_enabled=False).exclude(_next_run__isnull=True):
        dlog.debug("Setting _next_run to None on disabled job " +
                   str(j.id) + ", " + j.name)
        j._next_run = None
        j.save()

    # run Job.run() on each job
    # Filter to only enabled jobs and jobs under run count limit
    for j in Job.objects.filter(
            Q(job_enabled=True),                    # job_enabled is True AND
            Q(run_count_limit__isnull=True) |       # ( run_count_limit is None
            Q(_run_count__lt=F('run_count_limit'))  # OR run_count < limit )
    ):
        # debugRunCountMsg(j)
        worker(j.id)


# Ideas for future version:
# maybe learn how to catch the termination signal so daemon shutdown can be
#   logged.
# On linux the buffering makes it so you can't see the output of
#   akjobd.out right away. If debug is turned on, turn off the buffer or
#   greatly reduce the buffer.
def daemonize():
    with open(os.path.join(logdir, "akjobd.out"), "w+") as outfile:
        with daemon.DaemonContext(
                stdout=outfile, stderr=outfile,
                files_preserve=[akjob_logging.fh.stream, job_log_stream],
                pidfile=pid.PidFile(pidname=pidfile, piddir=piddir)):
            print("akjob daemon starting. ", str(datetime.now()))
            global dlog
            # dlog = get_daemon_logger()
            dlog = logger
            while True:
                # print(" " * 5, "=" * 21, str(datetime.now()), "=" * 21)
                print(" " * 5, "=" * 70)
                sys.stdout.flush()
                loop_through_jobs()
                print(" " * 5, "_" * 70)
                sys.stdout.flush()
                sleep(60)


# Next Version TODO: Check that the pid file is gone. If not, try again,
# possibly with SIGKILL.
def stop_daemon(pid):
    logger.info("Stopping Daemon. Sending SIGTERM to pid " + str(pid))
    os.kill(pid, 15)  # 15 = SIGTERM - "Software termination signal"

def start_daemon():
    logger.info("Starting the akjob daemon.")
    daemonize()

# To get the pid module to do this for me proved tricky. I'll get it myself.
def get_pid_from_pidfile():
    "Read the pid in the pidfile."
    filename = os.path.abspath(os.path.join(piddir, pidfile))
    with open(filename, "r") as fh:
        fh.seek(0)
        pid_str = fh.read(16).split("\n", 1)[0].strip()
        return int(pid_str)

# Before the daemon starts it checks the pid file but I can't monitor the
# results so here I'm doing a pre-check on the pidfile.
def pid_precheck():
    "Check the pidfile."
    # logger.debug("Pre-checking PID file.")
    pidcheck = pid.PidFile(pidname=pidfile, piddir=piddir)
    pidstatus = None
    try:
        pidstatus = pidcheck.check()
        if pidstatus:
            logger.info(pidstatus)
        if pidstatus == "PID_CHECK_NOFILE":
            return pidstatus
    # pid.PidFileAlreadyLockedError might also need to be handled.
    except pid.PidFileAlreadyRunningError as err:
        logger.info(err)
        return "AlreadyRunning"
    except:  # noqa: E722
        logger.error('Unknown pid related error: ' + str(sys.exc_info()[1:2]))
        raise SystemExit


def do_action(action):
    if action not in ["start", "stop", "restart"]:
        raise Exception("The do_action function requires start, stop, or "
                        "restart as an argument.")
    status = pid_precheck()
    if status == "AlreadyRunning":
        if action == "stop":
            stop_daemon(get_pid_from_pidfile())
        elif action == "restart":
            stop_daemon(get_pid_from_pidfile())
            sleep(2)
            start_daemon()
        if __name__ == '__main__':
            raise SystemExit
        else:
            return
    if action == "stop":
        if status == "PID_CHECK_NOFILE":
            logger.info("Stop command given but the pid file wasn't found.")
        else:
            stop_daemon(get_pid_from_pidfile())
            if __name__ == '__main__':
                raise SystemExit
            else:
                return
    elif action == "start":
        start_daemon()
    elif action == "restart":
        logger.info("restart command given but the pid file wasn't found.")
        start_daemon()
    else:
        logger.error("Didn't receive start or stop command.")


# set things up if ran from the command line or the subprocessing module from
# apps.py or tests.py.
if __name__ == '__main__':
    parse_args()
    setup_django()
    set_pid_file_name()
    set_pid_location()
    setup_logging()
    check_for_root()
    do_action(args.action)


# For setting things up when this module is imported.
# required to be used within the django context. django.setup() not ran.
def setup():
    setup_django()
    set_pid_file_name()
    set_pid_location()
    setup_logging()
