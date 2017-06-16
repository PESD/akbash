import subprocess
from django.apps import AppConfig
# import akjob.akjob_daemon


class AkjobConfig(AppConfig):
    name = 'akjob'

    def ready(self):
        "Start the daemon when akbash starts up."
        subprocess.run(['python', '/Users/robwirk/dev/akbash/akjob/akjobd.py'])
        pass
