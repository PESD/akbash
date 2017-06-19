import subprocess
from django.apps import AppConfig


class AkjobConfig(AppConfig):
    name = 'akjob'

    def ready(self):
        "Start the akjob daemon when akbash starts up."
        subprocess.run(['python', 'akjob/akjobd.py'])
