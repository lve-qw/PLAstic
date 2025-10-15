# cart/cart.py
from decimal import Decimal
from django.conf import settings
from catalog.models import Filament

class Cart:
    """Класс корзины, работающей через сессии"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, filament: Filament, quantity: int = 1, update_quantity: bool = False):
        """Добавить товар в корзину"""
        filament_id = str(filament.id) # type: ignore
        if filament_id not in self.cart:
            self.cart[filament_id] = {"quantity": 0, "price": str(filament.price)}
        if update_quantity:
            self.cart[filament_id]["quantity"] = quantity
        else:
            self.cart[filament_id]["quantity"] += quantity
        self.save()

    def save(self):
        """Сохранить изменения"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, filament: Filament):
        """Удалить товар из корзины"""
        filament_id = str(filament.id) # type: ignore
        if filament_id in self.cart:
            del self.cart[filament_id]
            self.save()

    def __iter__(self):
        """Перебор элементов корзины"""
        filament_ids = self.cart.keys()
        filaments = Filament.objects.filter(id__in=filament_ids)
        for filament in filaments:
            item = self.cart[str(filament.id)] # type: ignore
            item["filament"] = filament
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Количество товаров"""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Общая сумма"""
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        """Очистить корзину"""
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
