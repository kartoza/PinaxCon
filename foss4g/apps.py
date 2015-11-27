from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "foss4g"

    def ready(self):
        import_module("foss4g.receivers")
