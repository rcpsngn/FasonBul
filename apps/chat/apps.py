from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chat'
    verbose_name = 'Sohbet ve İletişim'

    def ready(self):
        from . import signals  # noqa: F401
