# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm

class RegisterView(CreateView):
    """Регистрация пользователя"""
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

class UserLoginView(LoginView):
    """Авторизация пользователя"""
    template_name = "accounts/login.html"

class UserLogoutView(LogoutView):
    """Выход пользователя"""
    next_page = reverse_lazy("core:home")

class ProfileView(TemplateView):
    """Личный кабинет"""
    template_name = "accounts/profile.html"
