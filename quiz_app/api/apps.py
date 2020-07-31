from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'quiz_app.api'
    label = 'api'

    def ready(self):
        from quiz_app.api import signals
