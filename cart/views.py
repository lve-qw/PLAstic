# cart/views.py
from django.shortcuts import redirect, render, get_object_or_404
from catalog.models import Filament
from .cart import Cart

def cart_detail(request):
    """Страница корзины"""
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})

def cart_add(request, filament_id):
    """Добавить товар в корзину"""
    cart = Cart(request)
    filament = get_object_or_404(Filament, id=filament_id)
    cart.add(filament=filament, quantity=1)
    return redirect("cart:detail")

def cart_remove(request, filament_id):
    """Удалить товар из корзины"""
    cart = Cart(request)
    filament = get_object_or_404(Filament, id=filament_id)
    cart.remove(filament)
    return redirect("cart:detail")
