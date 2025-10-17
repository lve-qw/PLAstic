# devices/admin.py
from django.contrib import admin
from .models import DeviceFilamentLevel


@admin.register(DeviceFilamentLevel)
class DeviceFilamentLevelAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления уровнями филамента устройств.
    """
    list_display = [
        'device_id',
        'username', 
        'filament_percent',
        'last_updated'
    ]
    list_filter = ['filament_percent', 'last_updated']
    search_fields = ['device__device_id', 'device__user__username']
    readonly_fields = ['last_updated']
    
    def device_id(self, obj):
        return obj.device.device_id
    device_id.short_description = 'ID устройства'
    
    def username(self, obj):
        return obj.device.user.username
    username.short_description = 'Пользователь'