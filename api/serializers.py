# api/serializers.py
from rest_framework import serializers
from accounts.models import Device
from devices.models import DeviceFilamentLevel
from orders.models import Order, OrderItem
from catalog.models import Filament


class DeviceOrderSerializer(serializers.Serializer):
    """
    Сериализатор для создания заказа от устройства.
    """
    device_id = serializers.CharField(max_length=16, required=True)
    
    def validate_device_id(self, value):
        """
        Проверяет существование устройства с указанным ID.
        """
        try:
            device = Device.objects.get(device_id=value)
        except Device.DoesNotExist:
            raise serializers.ValidationError("Устройство с указанным ID не найдено")
        return value


class SetFilamentSerializer(serializers.Serializer):
    """
    Сериализатор для установки уровня филамента.
    """
    device_id = serializers.CharField(max_length=16, required=True)
    filament_percent = serializers.IntegerField(
        required=True,
        min_value=0,
        max_value=100,
        help_text="Процент оставшегося филамента (0-100)"
    )
    
    def validate_device_id(self, value):
        """
        Проверяет существование устройства с указанным ID.
        """
        try:
            device = Device.objects.get(device_id=value)
        except Device.DoesNotExist:
            raise serializers.ValidationError("Устройство с указанным ID не найдено")
        return value


class FilamentLevelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уровня филамента устройства.
    """
    device_id = serializers.CharField(source='device.device_id', read_only=True)
    username = serializers.CharField(source='device.user.username', read_only=True)
    
    class Meta:
        model = DeviceFilamentLevel
        fields = ['device_id', 'username', 'filament_percent', 'last_updated']
        read_only_fields = ['last_updated']