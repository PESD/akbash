"""

Notes:
Some things to test:
    *   Jobs with deleteme flag are deleted
    *   Disabled jobs are not ran
    *   Errors are logged

Do we want to test the contents of logs or logging?
https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertLogs
"""
import os
import datetime
from django.test import TestCase
from unittest import skipIf
from django.conf import settings
from akjob.models import Job
# from akjob.models import load_DayOfMonth, load_DayOfWeek, load_Months
# from akjob.models import JobCallable
# from django.db import IntegrityError
from akjob import akjobd
from time import sleep
from subprocess import run, DEVNULL


""" Test for the pidfile. akjobd start and stop. Log files.
"""
@skipIf(os.environ.get("CIRCLECI") == "true",
        "Akjobd not tested under CircleCI.")
class AkjobdTestCase(TestCase):


    _testdir = os.path.join(settings.BASE_DIR, "akjob", "unittest")
    _pidname = "akjobd-unittest.pid"
    _pidfile = os.path.join(_testdir, _pidname)


    @classmethod
    def removeTestDir(cls):
        # delete the log files
        for logfilename in ["akjob.job.log", "akjobd.log", "akjobd.out"]:
            try:
                os.remove(os.path.join(cls._testdir, logfilename))
            except FileNotFoundError:
                pass

        # remove the testdir
        os.rmdir(cls._testdir)


    @classmethod
    def setUpClass(cls):
        # is there anyway this might run in prod db? that would be bad.
        Job.objects.all().delete()  # just in case. this shouldn't be needed.

        # create test directory where log and pid files will be placed.
        os.makedirs(cls._testdir)

        # akjobd configuration
        os.environ["AKJOB_START_DAEMON"] = "False"
        os.environ["AKJOB_PID_DIR"] = cls._testdir
        os.environ["AKJOB_PID_FILE"] = cls._pidname
        os.environ["AKJOB_LOG_DIR"] = cls._testdir
        akjobd.piddir = cls._testdir
        akjobd.pidfile = cls._pidname
        akjobd.logdir = cls._testdir
        akjobd.setup()


    @classmethod
    def tearDownClass(cls):
        # Make sure the unittest akjobd isn't running
        akjobd.do_action("stop")
        sleep(1)
        if os.path.isfile(cls._pidfile):
            raise Exception("Unittest akjobd PID file still exists.")
        cls.removeTestDir()


    # Needs to be ran in a separate process because it's going to deamonize and
    # detach from everything which would mess up testing.
    @classmethod
    def start_daemon(cls):
        run(["python", os.path.join(settings.BASE_DIR, "manage.py"), "akjobd",
             "start", "-pd", cls._testdir, "-pn", cls._pidname, "-ld",
             cls._testdir])


    def test_1_daemon_auto_start(self):
        # First stop the daemon if it's running.
        akjobd.do_action("stop")
        sleep(1)
        self.assertFalse(os.path.isfile(self._pidfile))
        # Environment variable so the daemon doesn't auto-start.
        os.putenv('AKJOB_START_DAEMON', "False")
        # Just running the management script should auto-start akjob.
        run(["python", os.path.join(settings.BASE_DIR, "manage.py")],
            stdout=DEVNULL)
        # check that the daemon didn't auto-start.
        self.assertFalse(os.path.isfile(self._pidfile))
        # Environment variable so the daemon does auto-start.
        os.putenv('AKJOB_START_DAEMON', "True")
        # Just running the management script should auto-start akjob.
        run(["python", os.path.join(settings.BASE_DIR, "manage.py")],
            stdout=DEVNULL)
        sleep(1)
        # check that the daemon did auto-start.
        self.assertTrue(os.path.isfile(self._pidfile))


    def test_2_stop_daemon(self):
        self.start_daemon()
        sleep(1)
        akjobd.do_action("stop")
        sleep(1)
        self.assertFalse(os.path.isfile(self._pidfile))


    def test_3_start_daemon(self):
        akjobd.do_action("stop")
        sleep(1)
        self.start_daemon()
        sleep(1)
        self.assertTrue(os.path.isfile(self._pidfile))

    # I can't think of a good way to test that akjobd will only run once. I
    # could read the pid in the pid file then start akjobd again then check if
    # the pid has changed. But is that really a good test?
    def test_4_daemon_run_once_only(self):
        akjobd.do_action("start")
        sleep(1)
        pid1 = akjobd.get_pid_from_pidfile()
        akjobd.do_action("start")
        sleep(1)
        pid2 = akjobd.get_pid_from_pidfile()
        self.assertEqual(pid1, pid2)


    # Check if log files exist and are not empty.
    def test_5_log_files_exist(self):
        akjobd.do_action("start")
        sleep(1)
        # there should be akjobd.log and akjobd.out but there may not be a
        # akjob.job.log since no jobs are scheduled.
        if (os.path.isfile(os.path.join(
                self._testdir, "akjobd.log")) is True and
            os.path.isfile(os.path.join(
                self._testdir, "akjobd.out")) is True):
            self.assertNotEqual(0, os.path.getsize(os.path.join(self._testdir,
                                                                "akjobd.out")))
            self.assertNotEqual(0, os.path.getsize(os.path.join(self._testdir,
                                                                "akjobd.log")))
        else:
            self.assertTrue(os.path.isfile(os.path.join(self._testdir,
                                                        "akjobd.log")))
            self.assertTrue(os.path.isfile(os.path.join(self._testdir,
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
        jx.active_time_tz_offset_timedelta = datetime.timedelta(
            days=2, hours=2, minutes=25)  # stored as 181500 in the DB
        jx.save()
        # refresh the field from the DB
        del jx.active_time_tz_offset_timedelta
        self.assertEqual(jx.active_time_tz_offset_timedelta,
                         datetime.timedelta(days=2, hours=2, minutes=25))

        # Checking the value stored in the DB
        with connection.cursor() as cursor:
            cursor.execute("select active_time_tz_offset_timedelta from "
                           "akjob_job where id=%s", [jx.id])
            row = cursor.fetchone()
            result = row[0]

        self.assertEqual(result, 181500)










""" Test scheduled jobs
"""

"""
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
        try:
            load_DayOfMonth()
            load_DayOfWeek()
            load_Months()
        except IntegrityError:
            pass



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
