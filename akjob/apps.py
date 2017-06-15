from django.apps import AppConfig
# import akjob.akjob_daemon


class AkjobConfig(AppConfig):
    name = 'akjob'

    def ready(self):
        "Start the daemon when akbash starts up."
        # akjob.akjob_daemon.start_daemon()
        pass
