# devices/apps.py
from django.apps import AppConfig


class DevicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devices'
    verbose_name = 'Устройства и мониторинг'
    
    def ready(self):
        """
        Импортируем сигналы при готовности приложения.
        """
        import devices.signals