""" This is ran in the daemon loop in akjob.akjobd. """

import sys
import os
import threading
# from akjob_logger import logger
from time import sleep


# I'm having difficulties because akjobd.py is ran without knowing anything
# about django and is not ran from the django site's base dir. So I'm having
# trouble importing from akjob.models. this is critical because unpickeling
# objects need to be able to find their type class correctly.
def setup_django(basedir=None):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akbash.settings")
    from django.conf import settings
    if basedir is None:
        base_dir = settings.BASE_DIR
    else:
        base_dir = basedir
    # make sure base_dir is at the start of sys.path
    if base_dir in sys.path:
        sys.path.remove(base_dir)
    sys.path.insert(0, base_dir)
    os.chdir(base_dir)
    global Job
    from akjob.models import Job


def worker(idnum):
    job = Job.objects.get(id=idnum)
    job.run()


def main():
    """
    setup_django(basedir)
    for j in Job.objects.all():
        t = threading.Thread(target=worker, args=(j.id,))
        t.start()
        sleep(1)
    """
