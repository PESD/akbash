"""
Things to test:
* daemon control and daemon start / stop
    * start command starts daemon
    * stop command stops daemon
    * if daemon is running don't start another one
"""

# import akjob.akjob
from datetime import datetime, timedelta, timezone, time, date
from akjob.models import Job, load_DayOfMonth, load_DayOfWeek, load_Months
from django.test import TestCase
from django.db import IntegrityError

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
        try:
            load_DayOfMonth()
            load_DayOfWeek()
            load_Months()
        except IntegrityError:
            pass

        self.now = datetime.now(tz=utc)
        self.future = datetime.now(tz=utc) + timedelta(minutes=5)
        self.past = datetime.now(tz=utc) - timedelta(minutes=5)
        self.pastday = datetime.now(tz=utc) - timedelta(days=1)

        ra1 = Job.objects.create(name="Run once job - now")
        ra1.dates_list = self.now
        ra2 = Job.objects.create(name="Run once job - future")
        ra2.dates.create(job_datetime=self.future)
        ra3 = Job.objects.create(name="Run once job - past")
        ra3.dates_list = [self.past, self.pastday]

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

        lat1 = Job.objects.create(
            name="Limit active time",
            run_every=timedelta(minutes=45),
            active_time_begin=time(2, 0),
            active_time_end=time(4, 0))
        lat2 = Job.objects.create(
            name="Limit active time",
            run_every=timedelta(minutes=45),
            active_time_begin=time(2, 0))

        rcl1 = Job.objects.create(
            name="Run count limit 1",
            run_count_limit=10,
            run_count=9)
        rcl2 = Job.objects.create(
            name="Run count limit 2",
            run_count_limit=10,
            run_count=11)

        at1 = Job.objects.create(
            name="Active time limit 1",
            active_time_begin=time(12, 0),
            active_time_end=time(14, 0))


    def test_find_jobs(self):
        pass
