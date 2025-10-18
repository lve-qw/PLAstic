# api/utils.py
from typing import Dict, Any, Optional
from accounts.models import Device
from devices.models import DeviceFilamentLevel


def get_device_by_id(device_id: str) -> Optional[Device]:
    """
    Находит устройство по ID.
    
    Args:
        device_id: ID устройства
        
    Returns:
        Device object или None если не найдено
    """
    try:
        return Device.objects.get(device_id=device_id)
    except Device.DoesNotExist:
        return None


def create_filament_order(device: Device) -> Dict[str, Any]:
    """
    Создает заказ филамента для устройства.
    
    Args:
        device: Объект устройства
        
    Returns:
        Словарь с результатом операции
    """
    from catalog.models import Filament
    from orders.models import Order, OrderItem
    
    try:
        filament = Filament.objects.get(id=1)
    except Filament.DoesNotExist:
        return {
            'success': False,
            'error': 'Филамент с ID=1 не найден'
        }
    
    if filament.stock <= 0:
        return {
            'success': False, 
            'error': 'Филамент отсутствует на складе'
        }
    
    # Создаем заказ
    user = device.user
    order = Order.objects.create(
        user=user,
        name=user.get_full_name() or user.username,
        email=user.email,
    )
    
    # Создаем позицию заказа
    OrderItem.objects.create(
        order=order,
        filament=filament,
        price=filament.price,
        quantity=1
    )
    
    # Обновляем остаток на складе
    filament.stock -= 1
    filament.save()
    
    return {
        'success': True,
        'order_id': order.id,
        'filament': f'{filament.brand} {filament.material} {filament.color}',
        'price': float(filament.price),
        'status': order.get_status_display()
    }


def update_filament_level(device: Device, filament_percent: int) -> Dict[str, Any]:
    """
    Обновляет уровень филамента для устройства.
    
    Args:
        device: Объект устройства
        filament_percent: Процент филамента (0-100)
        
    Returns:
        Словарь с результатом операции
    """
    filament_level, created = DeviceFilamentLevel.objects.get_or_create(
        device=device,
        defaults={'filament_percent': filament_percent}
    )
    
    if not created:
        filament_level.filament_percent = filament_percent
        filament_level.save()
    
    return {
        'success': True,
        'created': created,
        'filament_percent': filament_level.filament_percent,
        'last_updated': filament_level.last_updated
    }