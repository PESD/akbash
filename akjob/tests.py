"""
Things to test:
* daemon control and daemon start / stop
    * start command starts daemon
    * stop command stops daemon
    * if daemon is running don't start another one
"""

# import akjob.akjob
from datetime import datetime, timedelta, timezone, time
from akjob.models import Job, load_DayOfMonth, load_DayOfWeek
from django.test import TestCase

utc = timezone.utc
# mst = timezone(timedelta(hours=-7))


""" Test scheduled jobs
some things to test:
* Jobs with run time around now() are run now.
* Jobs with past run time but didn't run are ran now.
* Jobs with past run time are not ran now.
* Jobs with run times in the future are not run now.
* Disabled jobs are not ran.
"""

class JobsToRunTestCase(TestCase):
    "Test that akjob can figure out which jobs to run"

    def setUp(self):
        load_DayOfMonth()
        load_DayOfWeek()
        self.now = datetime.now(tz=utc)
        self.future = datetime.now(tz=utc) + timedelta(minutes=5)
        self.past = datetime.now(tz=utc) - timedelta(minutes=5)

        Job.objects.create(
            name="Run once job - now", run_once_at=self.now)
        Job.objects.create(
            name="Run once job - future", run_once_at=self.future)
        Job.objects.create(
            name="Run once job - past", run_once_at=self.past)

        Job.objects.create(
            name="Run every job", run_every=timedelta(minutes=5))

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


    def test_find_jobs(self):
        pass
