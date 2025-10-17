# devices/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Device
from .models import DeviceFilamentLevel


@receiver(post_save, sender=Device)
def create_device_filament_level(sender, instance, created, **kwargs):
    """
    Автоматически создает запись уровня филамента при создании устройства.
    """
    if created:
        DeviceFilamentLevel.objects.get_or_create(
            device=instance,
            defaults={'filament_percent': 100}  # Начальный уровень 100%
        )