# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Дополнительная информация о пользователе"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    address = models.TextField(verbose_name="Адрес доставки", blank=True)

    def __str__(self) -> str:
        return f"Профиль {self.user.username}"

class Device(models.Model):
    """Специальное устройство, привязанное к пользователю"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    device_id = models.CharField(max_length=16, unique=True, verbose_name="ID устройства")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"

    def __str__(self):
        return f"{self.device_id} (пользователь: {self.user.username})"
    
