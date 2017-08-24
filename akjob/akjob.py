""" This is what akjob.akjobd runs. """

import os
import threading
from time import sleep



# I'm having difficulties because akjobd.py is ran without knowing anything
# about django and is not ran from the django site's base dir. So I'm having
# trouble importing from akjob.models.
def setup_django(basedir):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akbash.settings")
    if basedir is None:
        raise("Django base dir is required.")
    os.chdir(basedir)
    from akjob.models import Job as x
    global Job
    Job = x


def worker(idnum):
    job = Job.objects.get(id=idnum)
    job.run()
    pass


def main(basedir):
    setup_django(basedir)
    for j in Job.objects.all():
        t = threading.Thread(target=worker, args=(j.id,))
        t.start()
        sleep(1)
