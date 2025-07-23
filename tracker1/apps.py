from django.apps import AppConfig


class Tracker1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker1'


def ready(self):
    import tracker1.signals  # import your signal file
