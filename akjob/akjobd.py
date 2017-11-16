""" The akjob daemon. """

import os
import sys
import argparse
import pid
import daemon
from time import sleep
from contextlib import redirect_stderr


""" Notes:
python-daemon asks for pylockfile but that package is depreciated. Instead I'm
using pid which is python-daemon compatible.

This module does not work from the command line although it's almost there. I
think maybe I need to import django into the global namespace from
setup_django(). Also something is going wrong when importing from akjob_logger.
I'm going to leave it alone for now and use the management command instead.

Ideas for future versions:
Would using signals to control things be helpful?
Is there someway better to track if a job is running or not. If things stop
while a job is running, the _job_running flag doesn't get turned off and the
job will no longer run.
Look into catching termination signals and how they could be used to end the
loop in a better way.
"""


# setup piddir and pidname from command line arguments.
def parse_args():
    global args
    parser = argparse.ArgumentParser()
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
    global django  # not sure if django in global is needed.
    import django
    if __name__ == '__main__':
        # chdir to the BASE_DIR so the akbash.settings module and the app
        # packages can be found by django.setup().
        set_pre_setup_base_dir()
        # print(pre_setup_base_dir)  # for debug
        # os.chdir(pre_setup_base_dir)
        # print(os.getcwd())  # for debug
        # print(sys.path)  # for debug
        if pre_setup_base_dir not in sys.path:
            sys.path.insert(0, pre_setup_base_dir)
            # print(sys.path)  # for debug
        django.setup()
    global BASE_DIR
    BASE_DIR = django.conf.settings.BASE_DIR
    # print(BASE_DIR)  # for debug
    # os.chdir(BASE_DIR)
    global Job
    from akjob.models import Job
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
        if args.pidname is None:
            pidfile = "akjobd.pid"
        else:
            pidfile = args.pidname
    except NameError:
        pidfile = "akjobd.pid"

def set_pid_location():
    global piddir
    try:
        if args.piddir is None:
            piddir = os.path.join(BASE_DIR, "akjob")
        else:
            piddir = args.piddir
    except NameError:
        piddir = os.path.join(BASE_DIR, "akjob")


def set_log_location():
    global logdir
    try:
        if args.logdir is None:
            logdir = os.path.join(BASE_DIR, "akjob", "logs")
        else:
            logdir = args.logdir
    except NameError:
        logdir = os.path.join(BASE_DIR, "akjob", "logs")


# Set up logging
def setup_logging():
    # TODO: change akjob logging so log file location is accepted as a paramater
    # django needs to be setup before importing akjob_logger. (this is ghetto)
    set_log_location()
    # try:
    #     from akjob_logger import AkjobLogging
    # except ModuleNotFoundError:  # noqa  My pyflake doesn't have this builtin.
    from akjob.akjob_logger import AkjobLogging

    global logger
    akjob_logging = AkjobLogging(name="akjob.akjobd", logfilename="akjobd.log",
                                 logdir=logdir, loglevel=loglevel)
    logger = akjob_logging.get_logger()

# A different logger to run inside the daemon process.
def get_daemon_logger():
    akjob_logging = AkjobLogging(  # noqa
        name="akjob.akjobd.daemon",
        logfilename="akjobd.daemon.log",
    )
    return akjob_logging.get_logger()


def worker(idnum):
    global dlog
    job = Job.objects.get(id=idnum)
    dlog.info("Starting job " + str(job.id) + ", " + job.name)
    try:
        job.run()
    except Exception as inst:
        dlog.error("Something went wrong with Job " + str(job.id) + ", " +
                   job.name + "\n    " + str(inst))


def loop_through_jobs():
    for j in Job.objects.filter(job_enabled=True):
        worker(j.id)


def delete_jobs():
    """ Delete Jobs with the deleteme flag set to True. """
    global dlog
    for j in Job.objects.filter(deleteme=True):
        dlog.info("Deleting job " + str(j.id) + ", " + j.name)
        j.delete()

# maybe learn how to catch the termination signal so daemon shutdown can be
# logged.
def daemonize():
    with daemon.DaemonContext(
            pidfile=pid.PidFile(pidname=pidfile, piddir=piddir)):
        # with open(os.path.join(
        global dlog
        dlog = get_daemon_logger()
        while True:
            delete_jobs()
            loop_through_jobs()
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
    except pid.PidFileAlreadyRunningError as err:
        logger.info(err)
        return "AlreadyRunning"
    except:
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
            sleep(1)
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


# Idea: Move everything under the else clause into a setup() function. Modify
# the akjobd management command to use setup(). That way the module can be
# imported with anything happening.
if __name__ == '__main__':
    parse_args()
    setup_django()
    set_pid_file_name()
    set_pid_location()
    setup_logging()
    do_action(args.action)
else:
    # required to be used within the django context. django.setup() not ran.
    setup_django()
    set_pid_file_name()
    set_pid_location()
    setup_logging()
