# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileUpdateForm
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth import logout
from django.shortcuts import redirect

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

def user_logout(request):
    logout(request)
    return redirect("core:home")

@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileUpdateForm(instance=self.request.user.profile)
        context["orders"] = self.request.user.orders.all()

        return context

    def post(self, request, *args, **kwargs):
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
        return self.get(request)
