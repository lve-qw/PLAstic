# api/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from accounts.models import Device
from catalog.models import Filament
from orders.models import Order, OrderItem
from devices.models import DeviceFilamentLevel
from .serializers import DeviceOrderSerializer, SetFilamentSerializer, FilamentLevelSerializer


class DeviceOrderView(APIView):
    """
    API endpoint для создания заказа филамента от устройства.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ без аутентификации
    
    def post(self, request):
        """
        Создает заказ филамента для пользователя, привязанного к устройству.
        
        Входные параметры:
        - device_id: ID устройства
        
        Логика:
        1. Находит устройство по device_id
        2. Находит пользователя, привязанного к устройству
        3. Создает заказ с филаментом ID=1
        4. Возвращает информацию о созданном заказе
        """
        serializer = DeviceOrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Неверные данные', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        device_id = serializer.validated_data['device_id']
        
        try:
            # Находим устройство
            device = Device.objects.get(device_id=device_id)
            user = device.user
            
            # Находим филамент с ID=1
            try:
                filament = Filament.objects.get(id=1)
            except Filament.DoesNotExist:
                return Response(
                    {'error': 'Филамент с ID=1 не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Проверяем наличие на складе
            if filament.stock <= 0:
                return Response(
                    {'error': 'Филамент отсутствует на складе'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Создаем заказ
            order = Order.objects.create(
                user=user,
                name=user.get_full_name() or user.username,
                email=user.email,
                # Можно добавить телефон и адрес из профиля пользователя
            )
            
            # Создаем позицию заказа
            order_item = OrderItem.objects.create(
                order=order,
                filament=filament,
                price=filament.price,  # Текущая цена филамента
                quantity=1  # Одна катушка по умолчанию
            )
            
            # Обновляем остаток на складе
            filament.stock -= 1
            filament.save()
            
            # Формируем ответ
            response_data = {
                'success': True,
                'message': 'Заказ успешно создан',
                'order_id': order.id,
                'filament': f'{filament.brand} {filament.material} {filament.color}',
                'price': float(filament.price),
                'status': order.get_status_display(),
                'created_at': order.created_at.isoformat()
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Device.DoesNotExist:
            return Response(
                {'error': 'Устройство не найдено'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Внутренняя ошибка сервера: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SetFilamentView(APIView):
    """
    API endpoint для установки уровня филамента устройства.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ без аутентификации
    
    def post(self, request):
        """
        Обновляет уровень филамента для устройства.
        
        Входные параметры:
        - device_id: ID устройства
        - filament_percent: процент оставшегося филамента (0-100)
        
        Логика:
        1. Находит устройство по device_id
        2. Создает или обновляет запись уровня филамента
        3. Возвращает обновленные данные
        """
        serializer = SetFilamentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Неверные данные', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        device_id = serializer.validated_data['device_id']
        filament_percent = serializer.validated_data['filament_percent']
        
        try:
            # Находим устройство
            device = Device.objects.get(device_id=device_id)
            
            # Создаем или обновляем уровень филамента
            filament_level, created = DeviceFilamentLevel.objects.get_or_create(
                device=device,
                defaults={'filament_percent': filament_percent}
            )
            
            if not created:
                filament_level.filament_percent = filament_percent
                filament_level.save()
            
            # Сериализуем данные для ответа
            response_serializer = FilamentLevelSerializer(filament_level)
            
            response_data = {
                'success': True,
                'message': 'Уровень филамента обновлен',
                'data': response_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Device.DoesNotExist:
            return Response(
                {'error': 'Устройство не найдено'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Внутренняя ошибка сервера: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetFilamentLevelView(APIView):
    """
    API endpoint для получения текущего уровня филамента устройства.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Возвращает текущий уровень филамента для устройства.
        """
        serializer = DeviceOrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Неверные данные', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        device_id = serializer.validated_data['device_id']
        
        try:
            device = Device.objects.get(device_id=device_id)
            
            try:
                filament_level = DeviceFilamentLevel.objects.get(device=device)
                serializer = FilamentLevelSerializer(filament_level)
                return Response(serializer.data)
            except DeviceFilamentLevel.DoesNotExist:
                return Response(
                    {'error': 'Данные об уровне филамента не найдены'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Device.DoesNotExist:
            return Response(
                {'error': 'Устройство не найдено'},
                status=status.HTTP_404_NOT_FOUND
            )