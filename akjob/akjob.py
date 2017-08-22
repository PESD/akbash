from time import time

""" Test class """
def sayhi():
    print("hi")

class Exp():

    def run(self):
        sayhi()
        print("Hello from Exp.")
        print(time())

    @staticmethod
    def hi():
        return sayhi()


"""

Notes / Brainstorming:
* Read all the job objects
* find which jobs needs executing
* execute the selected jobs

Do something to protect from running jobs that are already running.
"""


""" commenting everying out since none of this is used. I coded it into the Job
class instead.


# I think I want to run jobs in their own process. I don't know what i'm doing.
# import subprocess


from datetime import datetime, timezone
from django.db.models import Q
from akjob.models import Job


def dtfloor(dt):
    "Floor datetime to minute. i.e., zero out seconds and microseconds."
    return dt.replace(second=0, microsecond=0)


def schedule(job):
    "Populate Job.next_run with the datetime that job should next be ran."
    pass


def find_jobs():
    "Find jobs that should be ran now."

    utc = timezone.utc
    now = dtfloor(datetime.now(tz=utc))

    jobs = Job.objects.filter(
        Q(run_count_limit=None) | Q(run_count__lt=run_count_limit),
        job_enabled=True,
        job_running=False
    )


def pstatus():
    "Print a pretty version of the Job attributes and status."
    pass

def run():
    pass


if __name__ == '__main__':
    run()
"""
