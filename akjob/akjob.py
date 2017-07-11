"""

Notes / Brainstorming:
* Read all the job objects
* find which jobs needs executing
* execute the selected jobs

Do something to protect from running jobs that are already running.
"""

# I think I want to run jobs in their own process. I don't know what i'm doing.
# import subprocess

import pendulum
from django.db.models import Q
from akjob.models import Job

# look for jobs that need to be executed
now_dt = pendulum.now()
all_jobs = Job.objects.filter(
    enable=True
).filter(
    Q(run_count_limit=None) | Q(run_count__lt=run_count_limit)
)
