# api/urls.py
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path(
        'device/order',
        views.DeviceOrderView.as_view(),
        name='device-order'
    ),
    path(
        'device/set_filament', 
        views.SetFilamentView.as_view(),
        name='set-filament'
    ),
    path(
        'device/get_filament',
        views.GetFilamentLevelView.as_view(),
        name='get-filament'
    ),
]