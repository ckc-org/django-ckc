from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'testapp'

    def ready(self):
        # Import and register signal handlers here
        print(dir())
        from . import signal_handlers # noqa
