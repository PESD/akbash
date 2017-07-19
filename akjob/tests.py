"""
Things to test:
* daemon control and daemon start / stop
    * start command starts daemon
    * stop command stops daemon
    * if daemon is running don't start another one
"""

# import akjob.akjob
from datetime import datetime, timedelta, timezone, time
from akjob.models import Job
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

        Job.objects.create(
            name="Run Montly job 1", run_monthly="1,15",
            run_monthly_time=time(00, 30))
        Job.objects.create(
            name="Run Montly job 2", run_monthly=[2, 16],
            run_monthly_time=time(23, 30))
        Job.objects.create(
            name="Run Montly no time fail", run_monthly="7")


    def test_find_jobs(self):
        pass
