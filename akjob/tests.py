"""
Things to test:
* daemon control and daemon start / stop
    * start command starts daemon
    * stop command stops daemon
    * if daemon is running don't start another one
"""

import os
from django.test import TestCase
from django.conf import settings
from akjob.models import Job
# from datetime import datetime, timedelta, timezone, time, date
# from akjob.models import load_DayOfMonth, load_DayOfWeek, load_Months
# from akjob.models import JobCallable
# from django.db import IntegrityError
from akjob import akjobd
from time import sleep
from subprocess import run


""" Test for the pidfile
"""
class DaemonStartStopTestCase(TestCase):

    def setUp(self):
        self.pidfile = os.path.join(settings.BASE_DIR, "akjob", "akjobd.pid")
        Job.objects.all().delete()


    # Needs to be ran in a separate process because it's going to deamonize and
    # detach from everything which would mess up testing.
    @staticmethod
    def start_daemon():
        run(["python", os.path.join(settings.BASE_DIR, "manage.py"), "akjobd",
             "start"])


    def test_1_pidfile_exists(self):
        """The daemon should have auto started so the pidfile should exist.
           This is wrong since tests are supposed to be self contained."""
        self.assertTrue(os.path.isfile(self.pidfile))
        print("1")  # for debug


    def test_2_stop_daemon(self):
        self.start_daemon()
        sleep(1)
        akjobd.do_action("stop")
        sleep(1)
        self.assertFalse(os.path.isfile(self.pidfile))
        print("2")  # for debug


    def test_3_start_daemon(self):
        akjobd.do_action("stop")
        sleep(1)
        self.start_daemon()
        sleep(1)
        self.assertTrue(os.path.isfile(self.pidfile))
        print("3")  # for debug


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
