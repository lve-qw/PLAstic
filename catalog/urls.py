# catalog/urls.py
from django.urls import path
from .views import FilamentListView, FilamentDetailView

app_name = "catalog"

urlpatterns = [
    path("", FilamentListView.as_view(), name="list"),
    path("<int:pk>/", FilamentDetailView.as_view(), name="detail"),
]
