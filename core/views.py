# core/views.py
from django.views.generic import TemplateView

class HomeView(TemplateView):
    """Домашняя страница проекта"""
    template_name = "core/home.html"
