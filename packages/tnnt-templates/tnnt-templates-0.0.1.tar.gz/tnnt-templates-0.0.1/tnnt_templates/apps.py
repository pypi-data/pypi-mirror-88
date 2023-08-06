from django.apps import AppConfig
from . import __version__


class TnntTemplatesConfig(AppConfig):
    name = "tnnt_templates"
    label = "tnnt_templates"
    verbose_name = "Terra Nanotech Auth Templates v{}".format(__version__)
