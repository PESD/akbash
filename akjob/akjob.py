""" This module is not currently being used. Ignore below.
This is ran by the daemon loop in akjob.akjobd. """

import sys
import os
import threading
from time import sleep



# I'm having difficulties because akjobd.py is ran without knowing anything
# about django and is not ran from the django site's base dir. So I'm having
# trouble importing from akjob.models. this is critical because unpickeling
# objects need to be able to find their type class correctly.
def setup_django(basedir):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akbash.settings")
    if basedir is None:
        raise("Django base dir is required.")
    # make sure basedir is at the start of sys.path
    if basedir in sys.path:
        sys.path.remove(basedir)
    sys.path.insert(0, basedir)
    os.chdir(basedir)
    global Job
    from akjob.models import Job


def worker(idnum):
    job = Job.objects.get(id=idnum)
    job.run()


def main(basedir):
    setup_django(basedir)
    for j in Job.objects.all():
        t = threading.Thread(target=worker, args=(j.id,))
        t.start()
        sleep(1)
