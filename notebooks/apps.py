from django.apps import AppConfig


class NotebooksConfig(AppConfig):
    name = 'notebooks'

    def ready(self):
        from . import signals  # noqa
