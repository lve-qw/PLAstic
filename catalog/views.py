# catalog/views.py
from django.views.generic import ListView, DetailView
from .models import Filament

class FilamentListView(ListView):
    """Список всех филаментов"""
    model = Filament
    template_name = "catalog/filament_list.html"
    context_object_name = "filaments"

class FilamentDetailView(DetailView):
    """Детальная страница филамента"""
    model = Filament
    template_name = "catalog/filament_detail.html"
    context_object_name = "filament"
