# accounts/admin.py
from django.contrib import admin
from .models import UserProfile, Device
from devices.models import DeviceFilamentLevel


class DeviceFilamentLevelInline(admin.StackedInline):
    """
    Inline для отображения уровня филамента в админке устройства.
    """
    model = DeviceFilamentLevel
    can_delete = False
    verbose_name_plural = 'Уровень филамента'
    readonly_fields = ['last_updated']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления устройствами.
    """
    list_display = [
        'device_id', 
        'username', 
        'email',
        'filament_level',
        'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['device_id', 'user__username', 'user__email']
    inlines = [DeviceFilamentLevelInline]
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Пользователь'
    
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
    
    def filament_level(self, obj):
        try:
            return f"{obj.filament_level.filament_percent}%"
        except DeviceFilamentLevel.DoesNotExist:
            return "Не установлен"
    filament_level.short_description = 'Филамент'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username', 'phone']