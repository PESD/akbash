from django.apps import AppConfig
import akjob.daemon


class AkjobConfig(AppConfig):
    name = 'akjob'

    def ready(self):
        "Start the daemon when akbash starts up."
        akjob.daemon.main()
