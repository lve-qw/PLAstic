# orders/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # Заполняем из профиля
            profile = request.user.profile
            order.name = request.user.username
            order.email = request.user.email
            order.phone = profile.phone or "—"
            order.address = profile.address or "—"

            order.save()

            # сохраняем товары
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    filament=item["filament"],
                    price=item["price"],
                    quantity=item["quantity"]
                )

            cart.clear()
            return render(request, "orders/created.html", {"order": order})
    else:
        form = OrderCreateForm()

    return render(request, "orders/create.html", {"cart": cart, "form": form})
