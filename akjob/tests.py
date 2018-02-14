"""

Notes:
Some things to test:
    *   Jobs with deleteme flag are deleted
    *   Disabled jobs are not ran
    *   Errors are logged
    *   test if run count limit works
    *   test if delete_on_run_count_limit works

Do we want to test the contents of logs or logging?
https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertLogs
"""


import os
import sys
from django.test import TestCase
from unittest import skipIf
from django.conf import settings
from akjob.models import Job, JobCallable
from akjob import akjobd
from time import sleep
from subprocess import run, DEVNULL
from datetime import datetime, timezone, timedelta  # , time
# from django.db import IntegrityError


""" Setup the module so that a separate instance of akjobd is spawned that does
    not effect the default akjobd instance.
"""
def setUpModule():
    # Assign global variables defining pidfile name and directory where logs
    # and pidfile are stored.
    global testdir, pidname, pidfile, testfiles
    testdir = os.path.join(settings.BASE_DIR, "akjob", "unittest")
    pidname = "akjobd-unittest.pid"
    pidfile = os.path.join(testdir, pidname)
    # testfiles - A list of files to cleanup after testing
    testfiles = ["akjob.job.log", "akjobd.log", "akjobd.out"]

    # create test directory where log and pid files will be placed.
    os.makedirs(testdir)

    # akjobd configuration
    # This is require to run an alternate instance of akjobd
    os.environ["AKJOB_START_DAEMON"] = "False"
    os.environ["AKJOB_PID_DIR"] = testdir
    os.environ["AKJOB_PID_FILE"] = pidname
    os.environ["AKJOB_LOG_DIR"] = testdir
    akjobd.piddir = testdir
    akjobd.pidfile = pidname
    akjobd.logdir = testdir
    akjobd.setup()

    # Path to the python executable
    global akjob_python
    akjob_python = os.path.join(sys.prefix, "bin", "python")


def tearDownModule():
    # Make sure the unittest akjobd isn't running
    akjobd.do_action("stop")
    sleep(2)
    if os.path.isfile(pidfile):
        raise Exception("Unittest akjobd PID file still exists.")

    # delete the log files. delete test files.
    for logfilename in testfiles:
        try:
            os.remove(os.path.join(testdir, logfilename))
        except FileNotFoundError:
            pass

    # remove the testdir
    os.rmdir(testdir)


""" The akjob daemon needs to be ran in a separate process because it's going
    to deamonize and detach from everything which would mess up testing.
"""
def start_daemon():
    base = settings.BASE_DIR
    run([akjob_python, os.path.join(base, "akjob", "akjobd.py"),
         "start",
         "-pd", testdir, "-pn", pidname, "-ld", testdir,
         "-bd", base])


""" A function that can be used with JobCallable.
    Creates a file in the testdir named "name" and writes "text" into it.
"""
def file_print(name, text):
    with open(os.path.join(testdir, name), 'w') as f:
        f.write(text)


""" A custom job code object
"""
class CustomJCO:
    def __init__(self, action, filename=None, testname=None, text=None):
        self.action = action
        self.filename = filename
        self.testname = testname
        self.text = text


    def run(self, ownjob=None):

        text = ("Job " + str(ownjob.id) + " " + ownjob.name + " : " +
                self.testname + " : " + self.text + "\n")

        if self.action == "file_print":
            with open(os.path.join(testdir, self.filename), 'w') as f:
                f.write(text)
        elif self.action == "print":
            print(text)
        else:
            raise Exception("No action provided.")



""" Test for the pidfile. akjobd start and stop. Log files.
"""
@skipIf(os.environ.get("CIRCLECI") == "true",
        "Akjobd not tested under CircleCI.")
class AkjobdTestCase(TestCase):


    def test_1_daemon_auto_start(self):
        # First stop the daemon if it's running.
        akjobd.do_action("stop")
        sleep(2)
        self.assertFalse(os.path.isfile(pidfile))
        # Environment variable so the daemon doesn't auto-start.
        os.putenv('AKJOB_START_DAEMON', "False")
        # Just running the management script should auto-start akjob.
        run([akjob_python, os.path.join(settings.BASE_DIR, "manage.py")],
            stdout=DEVNULL)
        # check that the daemon didn't auto-start.
        self.assertFalse(os.path.isfile(pidfile))
        # Environment variable so the daemon does auto-start.
        os.putenv('AKJOB_START_DAEMON', "True")
        # Just running the management script should auto-start akjob.
        run([akjob_python, os.path.join(settings.BASE_DIR, "manage.py")],
            stdout=DEVNULL)
        sleep(2)
        # check that the daemon did auto-start.
        self.assertTrue(os.path.isfile(pidfile))


    def test_2_stop_daemon(self):
        start_daemon()
        sleep(2)
        akjobd.do_action("stop")
        sleep(2)
        self.assertFalse(os.path.isfile(pidfile))


    def test_3_start_daemon(self):
        akjobd.do_action("stop")
        sleep(2)
        start_daemon()
        sleep(2)
        self.assertTrue(os.path.isfile(pidfile))

    # I can't think of a good way to test that akjobd will only run once. I
    # could read the pid in the pid file then start akjobd again then check if
    # the pid has changed. But is that really a good test?
    def test_4_daemon_run_once_only(self):
        start_daemon()
        sleep(2)
        pid1 = akjobd.get_pid_from_pidfile()
        start_daemon()
        sleep(2)
        pid2 = akjobd.get_pid_from_pidfile()
        self.assertEqual(pid1, pid2)


    # Check if log files exist and are not empty.
    def test_5_log_files_exist(self):
        start_daemon()
        sleep(2)
        # there should be akjobd.log and akjobd.out but there may not be a
        # akjob.job.log since no jobs are scheduled.
        if (os.path.isfile(os.path.join(
                testdir, "akjobd.log")) is True and
            os.path.isfile(os.path.join(
                testdir, "akjobd.out")) is True):
            self.assertNotEqual(0, os.path.getsize(os.path.join(testdir,
                                                                "akjobd.out")))
            self.assertNotEqual(0, os.path.getsize(os.path.join(testdir,
                                                                "akjobd.log")))
        else:
            self.assertTrue(os.path.isfile(os.path.join(testdir,
                                                        "akjobd.log")))
            self.assertTrue(os.path.isfile(os.path.join(testdir,
                                                        "akjobd.out")))


""" Test the custom model fields
"""
# I think this might work in circleci
# @skipIf(os.environ.get("CIRCLECI") == "true",
#         "Akjobd not tested under CircleCI.")
class CustomModelFieldTestCase(TestCase):

    def test_TimeZoneOffsetField(self):
        from django.db import connection
        jx = Job.objects.create(name="Test TimeZoneOffsetField")
        jx.active_time_tz_offset_timedelta = timedelta(
            days=2, hours=2, minutes=25)  # stored as 181500 in the DB
        jx.save()
        # refresh the field from the DB
        del jx.active_time_tz_offset_timedelta
        self.assertEqual(jx.active_time_tz_offset_timedelta,
                         timedelta(days=2, hours=2, minutes=25))

        # Checking the value stored in the DB
        with connection.cursor() as cursor:
            cursor.execute("select active_time_tz_offset_timedelta from "
                           "akjob_job where id=%s", [jx.id])
            row = cursor.fetchone()
            result = row[0]

        self.assertEqual(result, 181500)


""" Test job code object execution
"""
class JobCodeObjectTestCase(TestCase):

    def test_JobCallable(self):
        testfilename = "test_JobCallable"
        testtext = ("Created by method test_JobCallable in test case"
                    " JobCodeObjectTestCase.\n")
        testfiles.append(testfilename)
        j1 = Job.objects.create(name="JobCallable Test")
        idnum = j1.id
        jco = JobCallable(file_print, testfilename, testtext)
        j1.job_code_object = jco
        j1.save()
        # refresh from db to make sure jco works after pickel and unpickel
        # process.
        del j1
        j1 = Job.objects.get(id=idnum)
        j1.job_code_object.run()
        with open(os.path.join(testdir, testfilename), 'r') as f:
            result = f.readline()
        self.assertEqual(result, testtext)


    def test_CustomJCO(self):
        testfilename = "test_CustomJCO"
        testfiles.append(testfilename)
        j2 = Job.objects.create(name="CustomJCO Test")
        idnum = j2.id
        jco = CustomJCO("file_print",
                        filename=testfilename,
                        testname="Custom JCO Test",
                        text="FDSA")
        testtext = ("Job " + str(idnum) + " " +
                    "CustomJCO Test : Custom JCO Test : FDSA\n")
        j2.job_code_object = jco
        j2.save()
        # refresh from db to make sure jco works after pickel and unpickel
        # process.
        del j2
        j2 = Job.objects.get(id=idnum)
        j2.job_code_object.run(ownjob=j2)
        with open(os.path.join(testdir, testfilename), 'r') as f:
            result = f.readline()
        self.assertEqual(result, testtext)


""" Test scheduled jobs
"""
@skipIf(os.environ.get("CIRCLECI") == "true",
        "Akjobd not tested under CircleCI.")
class JobSchedulingTestCase(TestCase):
    "Test that job scheduling works."


    # date and time variables. designed to be called inside a test method.
    def setDateTimeVars(self):
        self.utc = timezone.utc
        self.mst = timezone(timedelta(hours=-7))
        self.now = datetime.now(tz=self.utc)
        self.future = self.now + timedelta(minutes=30)
        self.past = self.now - timedelta(minutes=30)
        self.pastday = self.now - timedelta(days=1)
        self.tomorrow = self.now + timedelta(days=1)


    def setUp(self):
        self.setDateTimeVars()


    def test_dates(self):
        # job = Job.objects.create(name="test_dates")
        pass


""" old code left as an example but will be deleted.
class JobsToRunTestCase(TestCase):
    "Test that akjob can figure out which jobs to run"

    # date and time variables
    def setDateTimeVars(self):
        self.utc = timezone.utc
        self.mst = timezone(timedelta(hours=-7))
        self.now = datetime.now(tz=self.utc)
        self.future = datetime.now(tz=self.utc) + timedelta(minutes=30)
        self.past = datetime.now(tz=self.utc) - timedelta(minutes=30)
        self.pastday = datetime.now(tz=self.utc) - timedelta(days=1)
        self.tomorrow = datetime.now(tz=self.utc) + timedelta(days=1)


    # Ignoring IntegrityError because that's what you get when the data is
    # already loaded and you hit a primary key constraint. Should I do a
    # refresh instead?
    def setUp(self):


        ra1 = Job.objects.create(name="Job dates")
        ra1.dates_list = [self.past, self.now, self.future, self.pastday,
                          self.tomorrow]
        ra2 = Job.objects.create(name="Job dates - future")
        ra2.dates.create(job_datetime=self.future)
        ra2.dates.create(job_datetime=self.tomorrow)
        ra3 = Job.objects.create(name="Job dates - past")
        ra3.dates_list = [self.past, self.pastday]

        Job.objects.create(name="Reoccuring / Run every job",
                           run_every=timedelta(minutes=5))

        rmj1 = Job.objects.create(name="Run Monthly job 1",
                                  monthly_time=time(00, 30))
        rmj1.monthly_days.add(1, 15)
        rmj2 = Job.objects.create(name="Run Monthly job 2",
                                  monthly_time=time(12, 1))
        rmj2.monthly_days_list = [7, 28]
        rmj3 = Job.objects.create(name="Run Monthly no time fail")
        rmj3.monthly_days.add(7)

        rwj1 = Job.objects.create(name="Run Weekly job 1",
                                  weekly_time=time(00, 30))
        rwj1.weekly_days.add(2, 4, 6)
        rwj2 = Job.objects.create(name="Run Weekly job 2",
                                  weekly_time=time(12, 1))
        rwj2.weekly_days_list = [1, 7]
        rwj3 = Job.objects.create(name="Run Weekly no time fail")
        rwj3.weekly_days.add(3)

        lat1 = Job.objects.create(
            name="Limit active time",
            run_every=timedelta(minutes=45),
            active_time_begin=time(2, 0),
            active_time_end=time(4, 0))
        # this will be in it's own test to test for the exception.
        # lat2 = Job.objects.create(
        #     name="Limit active time",
        #     run_every=timedelta(minutes=45),
        #     active_time_begin=time(2, 0))

        rcl1 = Job.objects.create(
            name="Run count limit 1",
            run_count_limit=10,
            _run_count=9)
        rcl2 = Job.objects.create(
            name="Run count limit 2",
            run_count_limit=10,
            _run_count=11)

        at1 = Job.objects.create(
            name="Active time limit 1",
            active_time_begin=time(12, 0),
            active_time_end=time(14, 0))


    def test_find_jobs(self):
        pass
"""
