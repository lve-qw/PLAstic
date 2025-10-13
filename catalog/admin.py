# catalog/admin.py
from django.contrib import admin
from .models import Filament

@admin.register(Filament)
class FilamentAdmin(admin.ModelAdmin):
    """Настройки отображения модели Filament в админке"""
    list_display = ("brand", "material", "color", "price", "stock")
    search_fields = ("brand", "material", "color")
    list_filter = ("brand", "material", "color")
