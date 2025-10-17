# devices/models.py
from django.db import models
from django.contrib.auth.models import User


class DeviceFilamentLevel(models.Model):
    """
    Модель для отслеживания уровня филамента в устройстве.
    """
    device = models.OneToOneField(
        'accounts.Device',
        on_delete=models.CASCADE,
        related_name='filament_level',
        verbose_name="Устройство"
    )
    filament_percent = models.PositiveIntegerField(
        default=100,
        verbose_name="Остаток филамента (%)",
        help_text="Остаток филамента в процентах (0-100)"
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление"
    )

    class Meta:
        verbose_name = "Уровень филамента"
        verbose_name_plural = "Уровни филамента"

    def __str__(self):
        return f"{self.device.device_id}: {self.filament_percent}%"

    def save(self, *args, **kwargs):
        # Обеспечиваем, что процент в диапазоне 0-100
        if self.filament_percent > 100:
            self.filament_percent = 100
        elif self.filament_percent < 0:
            self.filament_percent = 0
        super().save(*args, **kwargs)