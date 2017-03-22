from django.apps import AppConfig


class BpmConfig(AppConfig):
    name = 'bpm'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import bpm.signals.signals
        
