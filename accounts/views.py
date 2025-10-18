# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileUpdateForm, DeviceForm
from .models import Device
from orders.models import Order
from devices.models import DeviceFilamentLevel

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

@login_required
def profile_view(request):
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    device_form = DeviceForm()

    if request.method == "POST":
        if "update_profile" in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
        elif "add_device" in request.POST:
            device_form = DeviceForm(request.POST)
            if device_form.is_valid():
                new_device = device_form.save(commit=False)
                new_device.user = request.user
                new_device.save()
                return redirect("accounts:profile")

    devices = request.user.devices.all()
    orders = Order.objects.filter(user_id=request.user.id)
    return render(
        request,
        "accounts/profile.html",
        {
            "profile_form": profile_form,
            "device_form": device_form,
            "devices": devices,
            "orders": orders
        },
    )
    
@login_required
def delete_device(request, device_id):
    device = get_object_or_404(Device, id=device_id, user=request.user)
    device.delete()
    return redirect("accounts:profile")