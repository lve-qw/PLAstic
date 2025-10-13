# catalog/views.py
from django.views.generic import ListView, DetailView
from .models import Filament

class FilamentListView(ListView):
    """Список всех филаментов с поиском и фильтрацией"""
    model = Filament
    template_name = "catalog/filament_list.html"
    context_object_name = "filaments"

    def get_queryset(self):
        """Фильтрация и поиск"""
        queryset = Filament.objects.all()
        q = self.request.GET.get("q")
        brand = self.request.GET.get("brand")
        material = self.request.GET.get("material")
        color = self.request.GET.get("color")

        if q:
            queryset = queryset.filter(description__icontains=q)

        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        if material:
            queryset = queryset.filter(material__icontains=material)

        if color:
            queryset = queryset.filter(color__icontains=color)

        return queryset

    def get_context_data(self, **kwargs):
        """Передаём список уникальных брендов/материалов/цветов для фильтров"""
        context = super().get_context_data(**kwargs)
        context["brands"] = Filament.objects.values_list("brand", flat=True).distinct()
        context["materials"] = Filament.objects.values_list("material", flat=True).distinct()
        context["colors"] = Filament.objects.values_list("color", flat=True).distinct()
        return context

class FilamentDetailView(DetailView):
    """Детальная страница филамента"""
    model = Filament
    template_name = "catalog/filament_detail.html"
    context_object_name = "filament"
